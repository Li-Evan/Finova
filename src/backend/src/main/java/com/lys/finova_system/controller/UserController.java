package com.lys.finova_system.controller;

import com.aliyuncs.dysmsapi.model.v20170525.SendSmsResponse;
import com.aliyuncs.exceptions.ClientException;
import com.lys.finova_system.domain.Code;
import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.domain.User;
import com.lys.finova_system.service.RedisService;
import com.lys.finova_system.service.UserService;
import com.lys.finova_system.service.utils.GenerateRandomCode;
import com.lys.finova_system.service.utils.SmsTool;
import io.micrometer.common.util.StringUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/users")
@Slf4j
public class UserController {
    @Autowired
    private UserService userService;
    @Autowired
    private RedisService redisService;

    private String tokenId = "TOKEN-USER-";

    @PostMapping("/login")
    public ResultJSON login(@RequestBody User user) {
        return userService.handleLogin(user);
    }

    @PostMapping("/register")
    public ResultJSON register(@RequestBody User user) {
        return userService.handleRegister(user);
    }

    @PostMapping("/sms/send")
    public ResultJSON sendSms(@RequestBody Map<String, Object> requestMap, HttpServletRequest request) throws ClientException {
        Map<String, Object> map = new HashMap<>();
        String phoneNumber = requestMap.get("phoneNumber").toString();
        // 调用工具栏中生成验证码的方法
        String code = GenerateRandomCode.generateVerifyCode(6);
        // 填充验证码
        String templateParm = "{\"code\":\"" + code + "\"}";
        // 传入手机号码及短信模板中的验证码占位符
        SendSmsResponse response = SmsTool.sendSms(phoneNumber, templateParm);

        // 存入map中返回给前端
        map.put("verifyCode", code);
        map.put("phoneNumber", phoneNumber);
        request.getSession().setAttribute("CodePhone", map);
        if (response.getCode().equals("OK")) {
            log.info("验证码发送成功");
            map.put("isOK", "OK");
            // 验证码绑定手机号并存储到redis
            redisService.set(tokenId + phoneNumber, code);
            // 设置过期时间为5分钟
            redisService.expire(tokenId + phoneNumber, 300);

            return new ResultJSON(Code.OK, true, "验证码发送成功");
        } else {
            log.error("验证码发送失败");
            map.put("isOK", "NOT_OK");

            return new ResultJSON(Code.BAD_REQUEST, false, "验证码发送失败");
        }
    }

    @PostMapping("/sms/login")
    public ResultJSON loginBySms(@RequestBody Map<String, Object> requestMap) {
        String phoneNumber = requestMap.get("phoneNumber").toString(); // 获取用户输入的手机号
        String verifyCode = requestMap.get("verifyCode").toString(); // 获取用户输入的验证码

        // 首先确认验证码是否失效
        String redisAuthCode = redisService.get(tokenId + phoneNumber); // 获取redis中的value
        if (StringUtils.isEmpty(redisAuthCode)) {
            // 未取到验证码则已过期
            log.error("验证码已过期");
            return new ResultJSON(Code.BAD_REQUEST, false, "验证码已过期，登录失败");
        } else if (!"".equals(redisAuthCode) && !verifyCode.equals(redisAuthCode)) {
            // redis中存的验证码不为空且验证码不正确
            log.error("验证码错误");
            return new ResultJSON(Code.BAD_REQUEST, false, "验证码错误，请重新输入");
        } else {
            log.info("验证码正确，处理登录");
            return userService.handleSms(phoneNumber);
        }

    }

    @PostMapping("/sms/bind")
    public ResultJSON bindPhoneNumber(@RequestBody Map<String, Object> requestMap) {
        String username = requestMap.get("username").toString(); // 获取当前操作用户的用户名
        String phoneNumber = requestMap.get("phoneNumber").toString(); // 获取用户输入的手机号
        String verifyCode = requestMap.get("verifyCode").toString(); // 获取用户输入的验证码

        // 首先确认验证码是否失效
        String redisAuthCode = redisService.get(tokenId + phoneNumber); // 获取redis中的value
        if (StringUtils.isEmpty(redisAuthCode)) {
            // 未取到验证码则已过期
            log.error("验证码已过期");
            return new ResultJSON(Code.BAD_REQUEST, false, "验证码已过期，绑定失败");
        } else if (!"".equals(redisAuthCode) && !verifyCode.equals(redisAuthCode)) {
            // redis中存的验证码不为空且验证码不正确
            log.error("验证码错误");
            return new ResultJSON(Code.BAD_REQUEST, false, "验证码错误，请重新输入");
        } else {
            log.info("验证码正确，处理绑定");
            return userService.handleBind(username, phoneNumber);
        }
    }
}
