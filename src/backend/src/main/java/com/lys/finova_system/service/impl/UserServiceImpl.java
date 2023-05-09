package com.lys.finova_system.service.impl;

import com.lys.finova_system.dao.UserDao;
import com.lys.finova_system.domain.Code;
import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.domain.ResultMsg;
import com.lys.finova_system.domain.User;
import com.lys.finova_system.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import io.micrometer.common.util.StringUtils;

@Service
@Slf4j
public class UserServiceImpl implements UserService {
    @Autowired
    private UserDao userDao;

    @Override
    public ResultJSON handleLogin(User user) {
        if (StringUtils.isBlank(user.getUsername()) || StringUtils.isBlank(user.getPassword())) {
            log.error("参数丢失");
            return new ResultJSON(Code.BAD_REQUEST, false, ResultMsg.LOSS.getMsg());
        }

        User temp = userDao.queryByUsername(user.getUsername());
        if (temp == null) {
            log.info("用户" + user.getUsername() + "不存在");
            return new ResultJSON(Code.NOT_FOUND, false, "用户不存在");
        } else if (!temp.getPassword().equals(user.getPassword())) {
            log.info(temp.getUsername() + "密码错误");
            return new ResultJSON(Code.BAD_REQUEST, false, "密码错误");
        } else {
            log.info("用户" + temp.getUid() + "登录成功");
            return new ResultJSON(Code.OK, temp.getUid(), ResultMsg.LOGIN_SUCCESS.getMsg());
        }
    }

    @Override
    public ResultJSON handleRegister(User user) {
        if (StringUtils.isBlank(user.getUsername()) || StringUtils.isBlank(user.getPassword())) {
            log.error("参数丢失");
            return new ResultJSON(Code.BAD_REQUEST, false);
        }

        User temp = userDao.queryByUsername(user.getUsername());
        Integer uid;
        if (temp != null) {
            log.info("用户" + user.getUsername() + "已存在");
            return new ResultJSON(Code.BAD_REQUEST, false, "用户已存在");
        } else if (user.getPhoneNumber() != null && userDao.insertUserWithPhoneNumber(user) > 0) {
            // 手机号注册
            uid = userDao.queryByPhoneNumber(user.getPhoneNumber()).getUid();
            log.info("手机号注册成功" + uid);
            return new ResultJSON(Code.OK, uid, ResultMsg.REGISTER_SUCCESS.getMsg());
        } else if (user.getPhoneNumber() == null && userDao.insertUser(user) > 0) {
            // 用户名密码注册
            uid = userDao.queryByUsername(user.getUsername()).getUid();
            log.info("用户名密码注册成功" + uid);
            return new ResultJSON(Code.OK, uid, ResultMsg.REGISTER_SUCCESS.getMsg());
        } else {
            log.error("注册失败");
            return new ResultJSON(Code.GONE, false, ResultMsg.REGISTER_ERROR.getMsg());
        }
    }

    @Override
    public ResultJSON handleSms(String phoneNumber) {
        if (StringUtils.isBlank(phoneNumber)) {
            log.error("参数丢失");
            return new ResultJSON(Code.BAD_REQUEST, false, "手机号为空");
        }

        User temp = userDao.queryByPhoneNumber(phoneNumber);
        if (temp == null) { // 若用户不存在，则注册，初始密码为1234567890
            log.info("注册成功，用户名、密码均为手机号" + phoneNumber);
            return handleRegister(new User(phoneNumber, phoneNumber, phoneNumber));
        } else { // 若用户已用手机号注册过，则直接登录
            log.info("登录成功" + temp.getUid());
            return new ResultJSON(Code.OK, temp.getUid(), ResultMsg.LOGIN_SUCCESS.getMsg());
        }
    }

    @Override
    public ResultJSON handleBind(String username, String phoneNumber) {
        if (StringUtils.isBlank(phoneNumber)) {
            log.error("参数丢失");
            return new ResultJSON(Code.BAD_REQUEST, false, "手机号为空");
        }

        User temp = userDao.queryByPhoneNumber(phoneNumber);
        if (temp == null) {
            // 该手机号没被绑定过
            log.info("手机号" + phoneNumber + "未被绑定");
            if (userDao.updatePhoneNumber(username, phoneNumber) > 0) {
                log.info("绑定成功");
                return new ResultJSON(Code.OK, true, "绑定成功");
            } else {
                log.error("绑定失败");
                return new ResultJSON(Code.GONE, false, "绑定失败");
            }
        } else {
            // 手机号被绑定了
            if (temp.getUsername().equals(username)) {
                log.error("该用户已绑定此手机号");
                return new ResultJSON(Code.BAD_REQUEST, false, "不能重复绑定");
            } else {
                log.error("该手机号已被别的用户绑定");
                return new ResultJSON(Code.BAD_REQUEST, false, "该手机号已被绑定");
            }
        }
    }
}
