package com.springboot.TodoWeb.todo;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.time.LocalDate;

@Service
public class TodoService {
    private static List<Todo> todos = new ArrayList<>();
    static {
        todos.add(new Todo(1,"Faisal", "347 Project", "Need to complete usage Scenario", false, LocalDate.now().plusDays(2)));
        todos.add(new Todo(2,"Faisal", "Trelet Project", "Need to complete", false, LocalDate.now().plusDays(20)));
        todos.add(new Todo(1,"Faisal",  "Trenza", "Need to complete the backend", false, LocalDate.now().plusMonths(2)));
    }

    public List<Todo> findByUserName(String username){
        return todos;
    }
}
