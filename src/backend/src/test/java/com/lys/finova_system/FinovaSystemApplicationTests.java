package com.lys.finova_system;

import com.lys.finova_system.service.QuatiAnaService;
import com.lys.finova_system.service.RedisService;
import com.lys.finova_system.service.utils.FinovaAlg;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

@SpringBootTest
class FinovaSystemApplicationTests {
    @Autowired
    private RedisService redisService;

    @Autowired
    private QuatiAnaService quatiAnaService;

    @Autowired
    private FinovaAlg finovaAlg;

    @Test
    public void testRedis() {
        redisService.set("test", "OK");
    }

    @Test
    public void testQA() {
//        quatiAnaService.test();
    }

    @Test
    public void testPresent() {
        String filePath = "宁德时代(300750)_资产负债表.CSV";
        try {
            String encodedFilename = URLEncoder.encode(filePath, "UTF-8");
            System.out.println(encodedFilename);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
    }
}
