package com.lys.finova_system.service.utils;

import com.aliyun.oss.ClientException;
import com.aliyun.oss.OSS;
import com.aliyun.oss.OSSException;
import com.aliyun.oss.model.ObjectMetadata;
import com.lys.finova_system.config.OSSConfiguration;
import lombok.extern.slf4j.Slf4j;
import org.apache.logging.log4j.util.Strings;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Date;
import java.util.UUID;

@Slf4j
@Component
public class OSSUtil {
    @Autowired
    private OSSConfiguration ossConfiguration;

    private final OSS ossClient = OSSConfiguration.getOssClient();

    public String uploadFileToOSS(String filePath) throws IOException{
        String fileName = null;

        // 生成一个随机的文件名(存储在图床的文件名)
        fileName = UUID.randomUUID().toString();
        File file = new File(filePath);
        InputStream inputStream = new FileInputStream(file);
        ObjectMetadata objectMetadata = new ObjectMetadata();
        objectMetadata.setContentLength(inputStream.available());
        objectMetadata.setContentType("image/png");
        objectMetadata.setCacheControl("no-cache");
        objectMetadata.setHeader("Pragma", "no-cache");
        objectMetadata.setContentDisposition("inline;filename=" + fileName);

        System.out.println(ossClient);
        System.out.println(ossConfiguration.getBucketName());
        System.out.println(fileName);
        System.out.println(inputStream);
        System.out.println(objectMetadata);

        // 上传文件
        log.info("上传文件到阿里云oss图床");
        ossClient.putObject(ossConfiguration.getBucketName(), fileName, inputStream, objectMetadata);

        return fileName;
    }

    public boolean doesObjectExist(String fileName) {
        try {
            if (Strings.isEmpty(fileName)) {
                log.error("文件名不能为空");
                return false;
            } else {
                return ossClient.doesObjectExist(ossConfiguration.getBucketName(), fileName);
            }
        } catch (OSSException | ClientException e) {
            e.printStackTrace();
        }
        return false;
    }

    public String getSingeNatureUrl(String filename, int expSeconds) {
        Date expiration = new Date(System.currentTimeMillis() + expSeconds * 1000L);
        URL url = ossClient.generatePresignedUrl(ossConfiguration.getBucketName(), filename, expiration);
        if (url != null) {
            return url.toString();
        }
        return null;
    }
}
