package com.faisal.fullstack_backend.crud.exception;

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id){
        super("Could not found the User with ID: "+ id);
    }
}
