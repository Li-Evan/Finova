package com.lys.finova_system.service.impl;

import com.lys.finova_system.dao.UploadFileDao;
import com.lys.finova_system.domain.Code;
import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.domain.ResultMsg;
import com.lys.finova_system.domain.UploadFile;
import com.lys.finova_system.service.LoadService;
import com.lys.finova_system.service.utils.FileUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.PostConstruct;
import java.io.*;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

@Service
@Slf4j
public class LoadServiceImpl implements LoadService {
    @Value("${upload.dir}")
    private String uploadDir; // 文件池前缀
    private final String[] fileTypes = {"stocks", "inquiry_letters", "annual_reports"};
    private final List<Path> paths = new ArrayList<>(); // 记录各种文件存储目录
    // 记录每个用户上传年报所需三个文件的进度(必须按顺序上传，或者前端按顺序发请求)
    private final Map<Integer, Integer> reportType = new HashMap<>();

    @Autowired
    private UploadFileDao uploadFileDao;

    @Value("${spring.profiles.active}")
    String active;
//    @Override
//    public void afterPropertiesSet() throws Exception {
//        init();
//    }

    @PostConstruct
    @Override
    public void init() {
        System.out.println(active);

        System.out.println(uploadDir);

        // 创建文件夹
        for (String file : fileTypes)  {
            // 完整文件池路径
            Path path = Paths.get(uploadDir + file);
            if (!Files.exists(path)) {
                try {
                    // 创建目录
                    Files.createDirectory(path);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            // 存储创建好的/已经存在的有效目录
            System.out.println(path);
            paths.add(path);
        }
    }

    // 获取指定的路径
    @Override
    public String getPath(Integer num) {
        return paths.get(num).toString();
    }

    private void uploadFile(MultipartFile file, String filePath, String fileDst) throws IOException {
        // 获取文件路径(不带文件名)
        if (filePath != null && !FileUtil.isDir(filePath)) {
            // 0和1都是单个文件，不需要获取前缀路径
            // 2是问询函上传的文件夹，需要先创建好前缀路径
            FileUtil.makeDirs(filePath);
            System.out.println("创建目录" + filePath);
        }

        log.info("拷贝文件到本地");
//        File newFile = new File(fileDst);
//        try {
//            InputStream inputStream = file.getInputStream();
//            InputStreamReader inputStreamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
//            OutputStream outputStream = new FileOutputStream(newFile);
//            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(outputStream, StandardCharsets.UTF_8);
//            char[] buffer = new char[1024];
//            int length;
//            while ((length = inputStreamReader.read(buffer)) != -1) {
//                outputStreamWriter.write(buffer, 0, length);
//            }
//            outputStreamWriter.close();
//            inputStreamReader.close();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }

//         获取文件路径(带文件名)
        File file_ = new File(fileDst);
        file_.createNewFile();
        file.transferTo(file_);
        System.out.println("文件存储在：" + fileDst);

        // Java 7的旧方法，真不行
//            Files.copy(file.getInputStream(), path);
//            System.out.println(path);
        // SpringMVC的好东西
//            file.transferTo(path); // 用MultipartFile的transferTo方法，将文件保存在本地
    }

    @Override
    public ResultJSON handleUploadFile(Integer uid, MultipartFile file, Integer fileType) {
        log.info("处理上传文件请求");
        log.info("处理文件" + fileType);

        if (file == null) return new ResultJSON(Code.BAD_REQUEST, false, ResultMsg.LOSS.getMsg());

        if (fileType < 0 || fileType > 2) return new ResultJSON(Code.BAD_REQUEST, false, ResultMsg.WRONG.getMsg());
//        Path path = this.paths.get(fileType).resolve(Objects.requireNonNull(file.getOriginalFilename()));
        String fileName = Objects.requireNonNull(file.getOriginalFilename());
        try {
            fileName = URLEncoder.encode(fileName, "UTF-8");
            System.out.println(fileName);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        String fileDst = getPath(fileType) + File.separator + fileName;

        try {
            // 上传文件
            uploadFile(file, null, fileDst);
            // 没抛异常就是成了
            log.info("文件拷贝到本地成功");
        } catch (IOException e) {
            log.error("文件拷贝到本地失败");
            // 若抛出异常则上传失败
            return new ResultJSON(Code.GONE, false, ResultMsg.UPLOAD_ERROR.getMsg());
        }

        // 根据上传文件类型来决定下一步操作
        UploadFile uploadFile = new UploadFile(Objects.requireNonNull(file.getOriginalFilename()), fileType, fileDst, uid);
        switch (fileType) {
            case 0:
                // 上传的是一支股票的历史价格数据
                // 将文件路径传到py函数中并返回一个全局股票序号
                Integer stock_num = 6; // 写死的 此处调用函数获取全局股票序号
                uploadFile.setFileNum(stock_num);
                break;
            case 1: // 上传的是问询函(单个文件)
                // 上传单个文件则设置file_num为1，代表后续调用算法的choice1
                Integer choice_num = 1;
                uploadFile.setFileNum(choice_num);
                break;
            case 2: // 上传的是年报三类文件之一
                // 不用操作
                // 记录年报三种文件，一定要三个文件都选择完再按顺序发请求上传
//                uploadFile.setFileNum(reportType.getOrDefault(uid, 1));
//                if (uploadFileDao.insert(uploadFile) < 0) {
//                    log.error("插入年报文件数据失败");
//                    return new ResultJSON(Code.GONE, false, ResultMsg.UPLOAD_ERROR.getMsg());
//                }
//                if (reportType.getOrDefault(uid, 1) < 3) {
//                    // 若还没上传到第三个文件就序号自增1
//                    reportType.put(uid, reportType.getOrDefault(uid, 1) + 1);
//                } else {
//                    // 若上传完三个文件则移除这条记录，下次再上传就从1开始重新计
//                    // 节省内存，有的用户可能只用一次
//                    reportType.remove(uid);
//                }
                break;
        }

        if (uploadFileDao.insert(uploadFile) < 0) {
            log.error("数据记录插入失败" + fileType);
            return new ResultJSON(Code.GONE, false, ResultMsg.UPLOAD_ERROR.getMsg());
        }
        log.info("插入问询函文件数据成功");
        log.info("fid为" + uploadFile.getFid());
        // 没报错就是成功
        return new ResultJSON(Code.OK, uploadFile.getFid(), ResultMsg.UPLOAD_SUCCESS.getMsg());
    }

    @Override
    public ResultJSON handleUploadFolder(Integer uid, MultipartFile[] folder, Integer folderType) {
        // 上传文件夹的本质也是上传文件
        if (folderType == 1) {
            // 上传的是问询函文件夹
            // 实在集成不进去了，单独处理
            String filePath = null;
            for (MultipartFile file : folder) {
                String fileName = Objects.requireNonNull(file.getOriginalFilename());
                if (fileName.endsWith(".pdf")) {
                    String fileDst = getPath(folderType) + File.separator + fileName;
                    filePath = getPath(folderType) + File.separator + fileName.substring(0, fileName.lastIndexOf("/"));

                    try {
                        // 上传文件
                        uploadFile(file, filePath, fileDst);
                    } catch (IOException e) {
                        log.error(fileName + "文件夹拷贝到本地失败");
                        // 若抛出异常则上传失败
                        return new ResultJSON(Code.GONE, false, ResultMsg.UPLOAD_ERROR.getMsg());
                    }
                }
            }
            log.info("文件夹拷贝到本地成功");
            if (filePath != null) {
                File file = new File(filePath);
                UploadFile uploadFile = new UploadFile(file.getName(), folderType, 2, filePath, uid);
                if (uploadFileDao.insert(uploadFile) < 0) {
                    log.error("插入问询函文件夹数据失败");
                    return new ResultJSON(Code.GONE, false, ResultMsg.UPLOAD_ERROR.getMsg());
                }
                log.info("插入问询函文件夹数据成功");
                return new ResultJSON(Code.OK, uploadFile.getFid(), ResultMsg.UPLOAD_SUCCESS.getMsg());
            } else {
                log.error("上传错误");
                return new ResultJSON(Code.GONE, false, ResultMsg.UPLOAD_ERROR.getMsg());
            }
        } else {
            // 只有问询函需要上传文件夹，年报不需要
            // 若有其他type出现则报错
            log.error("文件夹类型有误");
            return new ResultJSON(Code.BAD_REQUEST, null, ResultMsg.WRONG.getMsg());
        }
    }
}
