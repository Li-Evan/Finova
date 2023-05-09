package com.lys.finova_system.service;

import com.lys.finova_system.dao.UserDao;
import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.domain.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public interface UserService {

    ResultJSON handleLogin(User user);

    ResultJSON handleRegister(User user);

    ResultJSON handleSms(String phoneNumber);

    ResultJSON handleBind(String username, String phoneNumber);
}
