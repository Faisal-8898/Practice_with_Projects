package com.springboot.TodoWeb.todo;

import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.SessionAttributes;

import java.util.List;

@SessionAttributes("name")
@Controller
public class TodoController {
    private TodoService todoService;

    public TodoController(TodoService todoService){
        this.todoService = todoService;
    }

    @RequestMapping(value = "list-todo", method = RequestMethod.GET)
    public String listAllTodos(ModelMap model){
        List<Todo> todos = todoService.findByUserName("Faisal");
        model.addAttribute("todos", todos);
        return "listTodos";
    }
}
