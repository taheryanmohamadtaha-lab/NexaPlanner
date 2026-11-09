package com.nexaplanner.app.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "tasks")
data class TaskEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val title: String,
    val description: String = "",
    val startDate: Long,
    val priority: Int = 2,
    val status: Int = 0,
    val isPinned: Boolean = false
)
