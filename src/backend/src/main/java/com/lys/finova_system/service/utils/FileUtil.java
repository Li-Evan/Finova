package com.lys.finova_system.service.utils;

import com.alibaba.fastjson.JSON;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;

public class FileUtil {
    public static String getJsonFromFile(String filePath) throws IOException {
        File file = new File(filePath);
        if (!file.exists() || file.length() == 0) {
            return null;
        }
        String json;
        // 将文件内容读取为字符串
        json = FileUtils.readFileToString(file, "UTF-8");
//        System.out.println(json);
        return json;
    }

    public static boolean isFile(String filepath) {
        File f = new File(filepath);
        return f.exists() && f.isFile();
    }

    public static boolean isDir(String dirPath) {
        File f = new File(dirPath);
        return f.exists() && f.isDirectory();
    }

    /**
     * 创建多级目录
     * @param path
     */
    public static void makeDirs(String path) {
        File file = new File(path);
        // 如果文件夹不存在则创建
        if (!file.exists() && !file.isDirectory()) {
            file.mkdirs();
        }else {
            System.out.println("创建目录失败："+path);
        }
    }

    public static void writeJson(Object result, StringBuilder outputPathPrefix) throws IOException {
        String path = outputPathPrefix.toString() + "123.json";
        String json = JSON.toJSONString(result);
        FileWriter writer = new FileWriter(path);
        writer.write(json);
        Files.writeString(Paths.get(path), json);
    }
}
