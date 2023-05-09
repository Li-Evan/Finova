package com.lys.finova_system.config;

import com.aliyun.oss.OSS;
import com.aliyun.oss.OSSClientBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;

@Configuration
@Component
public class OSSConfiguration {

    private volatile static OSS ossClient;

    private volatile static OSSClientBuilder ossClientBuilder;

    private static String endpoint;

    private static String accessKeyId;

    private static String accessKeySecret;

    private static String urlPrefix;

    @Value("${aliyun.bucketName}")
    private String bucketName;

    @Value("${aliyun.endpoint}")
    public void setEndpoint(String endpoint) {
        OSSConfiguration.endpoint = endpoint;
    }

    @Value("${aliyun.accessKeyId}")
    public void setAccessKeyId(String accessKeyId) {
        OSSConfiguration.accessKeyId = accessKeyId;
    }

    @Value("${aliyun.accessKeySecret}")
    public void setAccessKeySecret(String accessKeySecret) {
        OSSConfiguration.accessKeySecret = accessKeySecret;
    }

    @Value("${aliyun.urlPrefix}")
    public void seturlPrefix(String urlPrefix) {
        OSSConfiguration.urlPrefix = urlPrefix;
    }

    public String getBucketName() {
        return bucketName;
    }

    @Bean
    @Scope("prototype")
    @PostConstruct
    public static OSS initOSSClient() {
        if (ossClient == null) {
            synchronized (OSSConfiguration.class) {
                if (ossClient == null) {
                    ossClient = initOSSClientBuilder().build(endpoint, accessKeyId, accessKeySecret);
                }
            }
        }
        return ossClient;
    }

    public static OSSClientBuilder initOSSClientBuilder() {
        if (ossClientBuilder == null) {
            synchronized (OSSConfiguration.class) {
                if (ossClientBuilder == null) {
                    ossClientBuilder = new OSSClientBuilder();
                }
            }
        }
        return ossClientBuilder;
    }

    public static OSS getOssClient() {
        return ossClient;
    }

    public static String getUrlPrefix() {
        return urlPrefix;
    }
}
