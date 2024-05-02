package com.springboot.TodoWeb.hello;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class Login {
    @RequestMapping
    public String login(){
        return "login";
    }
}
