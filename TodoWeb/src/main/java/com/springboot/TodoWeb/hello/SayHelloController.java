package com.springboot.TodoWeb.hello;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;


@Controller
public class SayHelloController {
    //say-hello -> "Hello! what are you learning today?"
    @RequestMapping("say-hello")
    @ResponseBody
    public String sayHello(){
        return "Hello! what are you learning today?";
    }


    @RequestMapping("hello-html")
    @ResponseBody
    public String sayHelloHtml(){
        StringBuffer sb = new StringBuffer();
        sb.append("<html>");
        sb.append("</html>");

        return sb.toString();
    }

    @RequestMapping("hello-jsp")
    public String sayHelloJsp(){
        return "sayHello";
    }
}
