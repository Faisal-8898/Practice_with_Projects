package com.faisal.fullstack_backend.crud.repository;

import com.faisal.fullstack_backend.crud.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
}
