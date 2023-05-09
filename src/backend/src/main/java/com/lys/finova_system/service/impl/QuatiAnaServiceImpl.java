package com.lys.finova_system.service.impl;

import com.lys.finova_system.dao.QuatiAnaDao;
import com.lys.finova_system.domain.AnalyzeChart;
import com.lys.finova_system.domain.Code;
import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.domain.ResultMsg;
import com.lys.finova_system.service.QuatiAnaService;
import com.lys.finova_system.service.utils.FileUtil;
import com.lys.finova_system.service.utils.FinovaAlg;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

@Service
@Slf4j
public class QuatiAnaServiceImpl implements QuatiAnaService {
    @Autowired
    private QuatiAnaDao quatiAnaDao;

    @Autowired
    private FinovaAlg finovaAlg;

    @Value("${output.presentPath}")
    private String presentOutputDir;

    @Override
    public void test() {
        System.out.println("测试");
    }


    @Override
    public ResultJSON handlePresent(Integer alg, Integer stock) throws IOException {
        log.info("处理呈现");
        // json文件名
        StringBuilder anaName = new StringBuilder();
        anaName.append("ana_").append(stock).append("_by_").append(alg);
        StringBuilder outputPathPrefix = new StringBuilder(); // 输出目录
        outputPathPrefix.append(presentOutputDir).append(File.separator)
                .append(anaName).append(File.separator);
        String dataPath = outputPathPrefix.toString() + "data.json";
        String buyPath = outputPathPrefix.toString() + anaName + "_buy.json";
        String sellPath = outputPathPrefix.toString() + anaName + "_sell.json";

        // 获取数据库中对应图的信息
        AnalyzeChart analyzeChart = quatiAnaDao.queryByAlgAndStock(alg, stock);
        System.out.println(analyzeChart);
        if (analyzeChart != null && analyzeChart.getState() == 1) {
            // 数据库中存在记录且图已生成
            log.info("数据库中存在记录且json已生成");
            // 直接从本地json文件中提取并返回
        } else if (analyzeChart != null && analyzeChart.getState() == 0) {
            // 数据库中存在记录但图未生成
            log.info("数据库中存在记录但json未生成");
            // 跑算法
            if (!finovaAlg.runPresent(alg, stock, outputPathPrefix.toString())) {
                log.error("算法运行出错");
                return new ResultJSON(Code.BAD_REQUEST, null, ResultMsg.ANA_ERROR.getMsg());
            }

            // 更新数据库记录(文件路径&状态)
//            System.out.println(analyzeChart.getAnalyzeName());
//            analyzeChart.setAnalyzeName(anaName.toString());
            analyzeChart.setState(1); // 更新算法分析状态
            analyzeChart.setPathPrefix(outputPathPrefix.toString());

            if (quatiAnaDao.updateStateAndOutputPath(analyzeChart) < 0) {
                log.error("数据更新失败");
                return new ResultJSON(Code.BAD_REQUEST, null, ResultMsg.ANA_ERROR.getMsg());
            }
            log.info("数据更新成功");
        } else {
            // 数据库中不存在记录则生成
            log.info("数据库中不存在记录则生成");
            // 跑算法
            if (!finovaAlg.runPresent(alg, stock, outputPathPrefix.toString())) {
                log.error("算法运行出错");
                // 插入记录但状态为0
                analyzeChart = new AnalyzeChart(anaName.toString(), 0, outputPathPrefix.toString(), alg, stock);
                quatiAnaDao.insertAnalyzeChart(analyzeChart);
                return new ResultJSON(Code.BAD_REQUEST, null, ResultMsg.ANA_ERROR.getMsg());
            }

            analyzeChart = new AnalyzeChart(anaName.toString(), 1, outputPathPrefix.toString(), alg, stock);
            // 新增数据库记录
            if (quatiAnaDao.insertAnalyzeChart(analyzeChart) < 0) {
                log.error("数据插入失败");
                return new ResultJSON(Code.BAD_REQUEST, null, ResultMsg.ANA_ERROR.getMsg());
            }
            log.info("数据插入成功");
        }

        HashMap<String, String> result = new HashMap<>(); // 返回的对象
        String dataJson = FileUtil.getJsonFromFile(dataPath); // 股票价格数据
        String buyJson = FileUtil.getJsonFromFile(buyPath); // 买入数据的json字串
        String sellJson = FileUtil.getJsonFromFile(sellPath); // 卖出数据的json字串
        if (dataJson != null && buyJson != null && sellJson != null) { // 都不为空才输出
            result.put("data", dataJson);
            result.put("buy", buyJson);
            result.put("sell", sellJson);
            log.info("json生成成功");
            FileUtil.writeJson(result, outputPathPrefix);
            return new ResultJSON(Code.OK, result, ResultMsg.ANA_SUCCESS.getMsg());
        } else {
            log.error("至少有一个json串为空");
            System.out.println("数据路径" + dataPath);
            System.out.println("买入文件路径：" + buyPath);
            System.out.println("卖出文件路径：" + sellPath);
            System.out.println("股票历史价格数据" + dataJson);
            System.out.println("买入json数据：" + buyJson);
            System.out.println("买入json数据：" + sellJson);
            return new ResultJSON(Code.BAD_REQUEST, null, ResultMsg.ANA_ERROR.getMsg());
        }
    }



    @Override
    public ResultJSON handlePredict(String filePath, Integer alg) {

        return null;
    }


}
