package com.springboot.TodoWeb.login;

import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.*;

@SessionAttributes("name")
@Controller
public class Login {
    AuthenticationService auth;

    public Login(AuthenticationService auth){
        this.auth = auth;
    }
    @RequestMapping(value = "login", method = RequestMethod.GET)
    public String login(){
        return "login";
    }
    @RequestMapping(value = "login", method = RequestMethod.POST)
    public String getWelcomePage(@RequestParam String name, @RequestParam String password, ModelMap modelMap){
        modelMap.put("name", name);
        if(auth.authenticate(name, password))  {
            modelMap.put("name", name);
            return "welcome";
        }

        else {
            modelMap.put("errorMessage", "Invalid userCredential");
            return "login";
        }
    }
}
