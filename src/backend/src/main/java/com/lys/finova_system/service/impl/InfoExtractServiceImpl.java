package com.lys.finova_system.service.impl;

import com.lys.finova_system.dao.UploadFileDao;
import com.lys.finova_system.domain.Code;
import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.domain.ResultMsg;
import com.lys.finova_system.domain.UploadFile;
import com.lys.finova_system.service.InfoExtractService;
import com.lys.finova_system.service.LoadService;
import com.lys.finova_system.service.utils.FileUtil;
import com.lys.finova_system.service.utils.FinovaAlg;
import com.lys.finova_system.service.utils.OSSUtil;
import lombok.extern.slf4j.Slf4j;
import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.Field;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Service
@Slf4j
public class InfoExtractServiceImpl implements InfoExtractService {
    @Autowired
    private UploadFileDao uploadFileDao;

    @Autowired
    private FinovaAlg finovaAlg;

    @Autowired
    private LoadService loadService;

    @Autowired
    private OSSUtil ossUtil;

    /**
     * @param fid     操作文件/文件夹的主键值
     * @param algType 算法类别：1--问询函(单个文件) 2--问询函(文件夹) 3--年报
     * @return
     */
    @Override
    public ResultJSON executeInquiryLetter(Integer fid, Integer algType) {
        // 先非空再空
        // 从数据库获取正在操作的文件对象
        UploadFile uploadFile = uploadFileDao.queryByFid(fid);

        if (uploadFile != null) {
            // 数据库中存在这个文件
            // 获取跑算法所需数据
            String input = uploadFile.getFilePath();
            String output;
            String fileName = uploadFile.getFileName();
            System.out.println(uploadFile);

            // 跑算法
            switch (algType) {
                case 1: // 单个文件问询函
                    output = loadService.getPath(algType) + File.separator + "output";
                    // 传入文件路径 在本地生成柱状图json和词云png
                    if (finovaAlg.analyzeInquiryLetter(input, output, 1)) {
                        // 词云本地png路径
                        String pngPath = output + File.separator + fileName.substring(0, fileName.lastIndexOf(".")) + "wordcloud.png";
                        String pngUrlString = null;
                        String json = null;
                        try {
                            System.out.println(pngPath);
                            String pngName = ossUtil.uploadFileToOSS(pngPath);
                            if (ossUtil.doesObjectExist(pngName)) {
                                log.info("文件在图床中存在");
                                pngUrlString = ossUtil.getSingeNatureUrl(pngName, 1000);
                            } else {
                                log.error("图床中不存在该文件");
                                return new ResultJSON(Code.GONE, false, ResultMsg.ANA_ERROR.getMsg());
                            }
                            // json的本地路径
                            String jsonPath = output + File.separator + fileName.substring(0, fileName.lastIndexOf(".")) + ".json";
                            json = FileUtil.getJsonFromFile(jsonPath);
                        } catch (IOException e) {
                            log.error("问询函::: pngurl或json生成失败");
                            System.out.println(pngUrlString);
                            System.out.println(json);
                            return new ResultJSON(Code.GONE, false, ResultMsg.ANA_ERROR.getMsg());
                        }
                        Map<String, String> result = new HashMap<>();
                        result.put("png", pngUrlString);
                        result.put("json", json);
                        return new ResultJSON(Code.OK, result, ResultMsg.ANA_SUCCESS.getMsg());
                    } else {
                        log.error("问询函::: 单个文件 算法运行失败");
                        return new ResultJSON(Code.GONE, false, ResultMsg.ANA_ERROR.getMsg());
                    }
                case 2: // 文件夹问询函
                    output = loadService.getPath(algType - 1) + File.separator + "output";
                    // 传入文件夹路径 导出csv文件
                    if (finovaAlg.analyzeInquiryLetter(input, output, 2)) {
                        // 本地csv路径
                        String csvPath = output + File.separator + "output.csv";
                        return new ResultJSON(Code.OK, csvPath, ResultMsg.ANA_SUCCESS.getMsg());
                    } else {
                        log.error("问询函::: 文件夹 算法运行失败");
                        return new ResultJSON(Code.GONE, false, ResultMsg.ANA_ERROR.getMsg());
                    }
                default:
                    // 算法选择有误
                    return new ResultJSON(Code.BAD_REQUEST, false, ResultMsg.WRONG.getMsg());
            }
        } else {
            // 按道理不应该没有
            return new ResultJSON(Code.GONE, false, ResultMsg.NOT_EXIST.getMsg());
        }
    }

    @Override
    public ResultJSON executeAnnualReport(Integer incomeFid, Integer cashflowFid, Integer assetsFid, Integer algType) {
        // 算法选择有误
        if (algType != 3) {
            log.error("年报算法序号选择有误");
            return new ResultJSON(Code.BAD_REQUEST, false, ResultMsg.WRONG.getMsg());
        }

        log.info("处理年报");
        // 依次获取数据库中三个数据表的记录
        UploadFile incomeTable = uploadFileDao.queryByFid(incomeFid);
        UploadFile cashflowTable = uploadFileDao.queryByFid(cashflowFid);
        UploadFile assetsTable = uploadFileDao.queryByFid(assetsFid);

        String data = null;
        if (incomeTable == null || cashflowTable == null || assetsTable == null ||
            incomeTable.getFilePath() == null || cashflowTable.getFilePath() == null || assetsTable.getFilePath() == null) {
            log.error("某个记录不存在");
            System.out.println(incomeTable);
            System.out.println(cashflowTable);
            System.out.println(assetsTable);
            // 有一个不存在就寄了
            return new ResultJSON(Code.GONE, false, ResultMsg.NOT_EXIST.getMsg());
        } else {
            // 跑算法生成各种率的数据
            data = finovaAlg.analyzeAnnualReport(incomeTable.getFilePath(), cashflowTable.getFilePath(), assetsTable.getFilePath());
            if (data != null) {
                /**
                 * [[3.988253448085262, 5.343634791728096, 0.5467454242928452, 0.18627498767475972, 2521.2304301605027, 2022.163071193426],
                 *  [0.9637007564385578, 0.10941752432344044, 0.12042182356307743, 0.055669123960066555, 13.697827996517523],
                 *  [1.3108108108108107, 1.0517942608108108, 2.3954802259887007],
                 *  [3.689131252746641, 0.04720248543795687, 2.3954802259887007, 0.9543030051120504]]
                 */
                data = data.substring(data.indexOf('['), data.length());
                log.info("年报::: 算法运行成功");
                return new ResultJSON(Code.OK, data, ResultMsg.ANA_SUCCESS.getMsg());
            } else {
                log.error("年报::: 算法运行失败");
                return new ResultJSON(Code.GONE, false, ResultMsg.ANA_ERROR.getMsg());
            }
        }
    }
}
