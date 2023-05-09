package com.lys.finova_system.service.utils;

import lombok.SneakyThrows;
import org.apache.commons.lang3.tuple.ImmutableTriple;
import org.apache.commons.lang3.tuple.MutableTriple;
import org.apache.commons.lang3.tuple.Triple;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

@Service
public class FinovaAlg {
    @Value("${alg.pyPath}")
    private String pyPath; // 运行算法所需的python路径
    @Value("${alg.algDir}")
    private String algDir; // 算法所在目录
    private String presentAlgName = "choiceAlgorithm.py"; // 呈现算法py文件名
    private String inquiryLetterAlgName = "main.py"; // 问询函算法py文件名
    private String annualReportAlgName = "main.py"; // 年报算法py文件名
    private String[] algPath = {
            File.separator + "QuantitativeTrading" + File.separator + "model" + File.separator,
            File.separator + "InfomationExtraction" + File.separator + "InquiryLetter" + File.separator,
            File.separator + "InfomationExtraction" + File.separator + "annualReport" + File.separator
    };
    private String presentAlgDir;
    private String inquiryLetterAlgDir;
    private String annualReportAlgDir;

    @PostConstruct
    public void init() {
        presentAlgDir = algDir + algPath[0];
        inquiryLetterAlgDir = algDir + algPath[1];
        annualReportAlgDir = algDir + algPath[2];

        System.out.println(presentAlgDir);
        System.out.println(inquiryLetterAlgDir);
        System.out.println(annualReportAlgDir);
    }

    // 调用命令行运行命令
    private Triple<Integer, String, String> runCMD(String cmd, String dir) {
        String outputPrefix = dir + ":::  运行：";

        StringBuilder std = new StringBuilder();
        StringBuilder err = new StringBuilder();

        Process p;
        System.out.println(outputPrefix + cmd);
        try {
            //执行命令
            p = Runtime.getRuntime().exec(cmd, null, new File(dir));
            //获取输出流，并包装到BufferedReader中
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader stderrReader = new BufferedReader(new InputStreamReader(p.getErrorStream()));
            Thread t1 = new Thread(new Runnable() { // 线程1打印标准输出流
                @SneakyThrows
                @Override
                public void run() {
                    String[] line = new String[1];
                    while ((line[0] = br.readLine()) != null) {
                        System.out.println(outputPrefix + "\tSTD OUTPUT：" + line[0]);
                        std.append(line[0]);
                    }
                }
            });

            Thread t2 = new Thread(new Runnable() { // 线程2打印标准错误流
                @SneakyThrows
                @Override
                public void run() {
                    String[] line = new String[1];
                    while ((line[0] = stderrReader.readLine()) != null) {
                        System.out.println(outputPrefix + "\tERR OUTPUT：" + line[0]);
                        err.append(line[0]);
                    }

                }
            });
            t1.start();
            t2.start();
            System.out.println(outputPrefix + "等待cmd执行结束");
            int exitValue = p.waitFor();
            stderrReader.close();
            br.close();
            System.out.println(outputPrefix + "  进程返回值：" + exitValue);
            return new ImmutableTriple<>(exitValue, std.toString(), err.toString());
        } catch (IOException | InterruptedException e) {
            System.out.println(outputPrefix + "  cmd 运行失败");
            e.printStackTrace();
        }

        return new ImmutableTriple<>(-1, null, null);
    }

    //---------------- 量化交易模块 ----------------//

    // 运行呈现算法
    public Boolean runPresent(Integer algNum, Integer stockNum, String outputDir) {
        if (stockNum == 0) stockNum = Integer.parseInt(GenerateRandomCode.generateVerifyCode(1, "12345"));
        if (algNum == 0) algNum = Integer.parseInt(GenerateRandomCode.generateVerifyCode(1, "1234"));

        // 复杂表达式中拼接字符串
        // bad
        // String cmd = pyPath + " " + algDir + presentAlg + " -dst \"" + outputPath + "\" -algorithm " + algNum + " -share " + stockNum;

        // good
        StringBuilder cmd = new StringBuilder();
        cmd.append(pyPath).append(" ").append(presentAlgName).append(" -dst ")
                .append(outputDir).append(" -algorithm ")
                .append(algNum).append(" -share ").append(stockNum);

        System.out.println("运行命令" + cmd);

        return runCMD(cmd.toString(), presentAlgDir).getLeft() == 0;
    }

    //---------------- 信息抽取模块 ----------------//

    // 问询函
    public Boolean analyzeInquiryLetter(String input, String output, Integer choice) {
        StringBuilder cmd = new StringBuilder();
        cmd.append(pyPath).append(" ").append(inquiryLetterAlgName).append(" -src ")
                .append(input);
        switch (choice) {
            case 1:
                // 单个文件问询函，生成词云png和柱状图json
                // 因此需要指定imgdst和jsondst
                cmd.append(" -imgdst ").append(output).append(" -jsondst ")
                        .append(output).append(" -choice ").append(choice);
                break;
            case 2:
                // 文件夹(多个文件)问询函，生成merge的csv文件
                // 因此需要指定merge_csv_dst
                cmd.append(" -merge_csv_dst ").append(output)
                        .append(" -xlsxdst ").append(output)
                        .append(" -choice ").append(choice);
                break;
            default:
                // 若选择不是以上两种则返回false
                return false;
        }

        System.out.println("运行命令" + cmd);

        return runCMD(cmd.toString(), inquiryLetterAlgDir).getLeft() == 0;
    }

    

    // 年报
    public String analyzeAnnualReport(String incomePath, String cashflowPath, String assetsPath) {
        StringBuilder cmd = new StringBuilder();
        cmd.append(pyPath).append(" ").append(annualReportAlgName).append(" -income_path ")
                .append(incomePath).append(" -cashflow_path ").append(cashflowPath)
                .append(" -assets_path ").append(assetsPath);

        Triple<Integer, String, String> triple = runCMD(cmd.toString(), annualReportAlgDir);

        return triple.getLeft() == 0 ? triple.getMiddle() : null;
    }
}
