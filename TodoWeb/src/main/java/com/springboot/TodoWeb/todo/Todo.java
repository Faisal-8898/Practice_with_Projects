package com.springboot.TodoWeb.todo;

import java.time.LocalDate;

// we need to have a database it can be my sql or oracle
// First we think to store the data in static database . then optimized it to database like sql or oracle
public class Todo {
    private int id;
    private String username;
    private String title;
    private String description;
    private LocalDate targetDate;
    private Boolean done;

    public Todo(int id, String username, String title, String description, Boolean done, LocalDate targetDate) {
        this.id = id;
        this.username = username;
        this.title = title;
        this.description = description;
        this.done = done;
        this.targetDate = targetDate;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDate getTargetDate() {
        return targetDate;
    }

    public void setTargetDate(LocalDate targetDate) {
        this.targetDate = targetDate;
    }

    public Boolean getDone() {
        return done;
    }

    public void setDone(Boolean done) {
        this.done = done;
    }

    @Override
    public String toString() {
        return "Todo{" + "id=" + id + ", username='" + username + '\'' + ", title='" + title + '\'' + ", description='" + description + '\'' + ", targetDate=" + targetDate + ", done=" + done + '}';
    }
}
