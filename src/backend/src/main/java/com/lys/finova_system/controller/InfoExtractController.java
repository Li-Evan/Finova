package com.lys.finova_system.controller;


import com.aliyun.core.utils.IOUtils;
import com.lys.finova_system.domain.Code;
import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.domain.ResultMsg;
import com.lys.finova_system.service.InfoExtractService;
import com.lys.finova_system.service.utils.FileUtil;
import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.*;
import org.springframework.util.AntPathMatcher;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.HandlerMapping;

import javax.servlet.http.HttpServletRequest;
import java.io.*;

@RestController
@RequestMapping("/infoExtractions")
public class InfoExtractController {
    @Autowired
    private InfoExtractService infoExtractService;

    @PostMapping("/extract/**")
    public Object extractInfo(HttpServletRequest request) throws IOException {
//        Integer fid, Integer algType
        String path = (String) request.getAttribute(HandlerMapping.PATH_WITHIN_HANDLER_MAPPING_ATTRIBUTE);
        String bestMatchPattern = (String) request.getAttribute(HandlerMapping.BEST_MATCHING_PATTERN_ATTRIBUTE);
        String subPath = new AntPathMatcher().extractPathWithinPattern(bestMatchPattern, path);

        // 从请求中获取参数
        Integer fid = Integer.parseInt(request.getParameter("fid"));
        Integer algType = Integer.parseInt(request.getParameter("algType"));

        // 跳转
        if (subPath.startsWith("/inquiry/file")) {
            return extractInquiryLetterFromFile(fid, algType);
        } else if (subPath.startsWith("/inquiry/folder")) {
            return extractInquiryLetterFromFolder(fid, algType);
        } else if (subPath.startsWith("/annualReport")) {
            Integer incomeFid = Integer.parseInt(request.getParameter("incomeFid"));
            Integer cashflowFid = Integer.parseInt(request.getParameter("cashflowFid"));
            Integer assetsFid = Integer.parseInt(request.getParameter("assetsFid"));
            return extractAnnualReportFromTables(incomeFid, cashflowFid, assetsFid, algType);
        } else {
            return new ResultJSON(Code.BAD_REQUEST, false, ResultMsg.WRONG.getMsg());
        }
    }

    @PostMapping("/extract/inquiry/file")
    public ResultJSON extractInquiryLetterFromFile(Integer fid, Integer algType) {
        return infoExtractService.executeInquiryLetter(fid, algType);
    }
//    public ResponseEntity<MultiValueMap<String, Object>> extractInquiryLetterFromFile(Integer fid, Integer algType) throws IOException {
//        HttpHeaders headers = new HttpHeaders(); // 新建相应头
//        headers.setContentType(MediaType.MULTIPART_MIXED); // 设置响应类型
//
//        // 混合值Map
//        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
//
//        // 获取json和png路径
//        System.out.println(fid);
//        System.out.println(algType);
//        ResultJSON result = infoExtractService.executeInquiryLetter(fid, algType);
//        if (result.getCode() != 200) {
//            return new ResponseEntity<>(body, headers, HttpStatus.BAD_REQUEST);
//        }
//        // 若为空则不会返回200
//        Pair<String, String> pair = (Pair) result.getData();
//
//        // 添加 JSON 数据
//        String json = FileUtil.getJsonFromFile(pair.getValue1());
//        HttpEntity<String> jsonEntity = new HttpEntity<>(json, headers);
//        body.add("json", jsonEntity);
//
//        // 添加图片文件流
//        InputStream imageStream = new FileInputStream(pair.getValue0());
//        byte[] imageBytes = IOUtils.toByteArray(imageStream);
//        ByteArrayResource imageResource = new ByteArrayResource(imageBytes) {
//            @Override
//            public String getFilename() {
//                return "image.png";
//            }
//        };
//        HttpHeaders imageHeaders = new HttpHeaders();
//        imageHeaders.setContentType(MediaType.IMAGE_PNG);
//        HttpEntity<ByteArrayResource> imageEntity = new HttpEntity<>(imageResource, imageHeaders);
//        body.add("image", imageEntity);
//
//        return new ResponseEntity<>(body, headers, HttpStatus.OK);
//    }

    @PostMapping("/extract/inquiry/folder")
    public ResponseEntity<InputStreamResource> extractInquiryLetterFromFolder(Integer fid, Integer algType) throws FileNotFoundException {
        String filePath = (String) infoExtractService.executeInquiryLetter(fid, algType).getData(); // 本地 CSV 文件的路径

        // 获取本地文件流，封装为InputStreamResource对象
        File file = new File(filePath);
        if (!file.exists() || file.length() == 0) {
            return ResponseEntity.badRequest().body(null);
        }

        InputStream inputStream = new FileInputStream(file);
        InputStreamResource resource = new InputStreamResource(inputStream);

        // 设置响应头
        HttpHeaders headers = new HttpHeaders();
        // 在浏览器中以附件形式返回，而不是直接打开
        headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + file.getName());
        headers.add(HttpHeaders.CONTENT_TYPE, "text/csv");

        return ResponseEntity.ok()
                .headers(headers)
                .contentLength(file.length())
                .contentType(MediaType.parseMediaType("application/octet-stream"))
                .body(resource);
    }

    @PostMapping("/extract/annualReport")
    public ResultJSON extractAnnualReportFromTables(Integer incomeFid, Integer cashflowFid, Integer assetsFid, Integer algType) {
        return infoExtractService.executeAnnualReport(incomeFid, cashflowFid, assetsFid, algType);
    }
}
