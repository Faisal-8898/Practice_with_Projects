package com.faisal.fullstack_backend.crud.controller;

import com.faisal.fullstack_backend.crud.entity.User;
import com.faisal.fullstack_backend.crud.exception.UserNotFoundException;
import com.faisal.fullstack_backend.crud.repository.UserRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.PostMapping;

@RestController
@CrossOrigin("http://localhost:3000/")
public class UserController {
  @Autowired private UserRepository userRepository;

  @PostMapping("/user")
  User newUser(@RequestBody User newUser) {
    return userRepository.save(newUser);
  }

  @GetMapping("/users")
  List<User> getAllUsers() {
    return userRepository.findAll();
  }

  @GetMapping("/user/{id}")
  public User getUserById(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow(() -> new UserNotFoundException(id));
  }

  @PutMapping("/user/{id}")
  User updateUser(@RequestBody User updatedUser, @PathVariable Long id) {
    return userRepository
        .findById(id)
        .map(
            user -> {
              user.setName(updatedUser.getName());
              user.setUsername(updatedUser.getUsername());
              user.setEmail(updatedUser.getEmail());
              return userRepository.save(user);
            })
        .orElseThrow(() -> new UserNotFoundException(id));
  }
}
