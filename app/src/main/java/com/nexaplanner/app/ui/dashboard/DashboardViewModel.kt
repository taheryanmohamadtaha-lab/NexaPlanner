package com.nexaplanner.app.ui.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nexaplanner.app.data.local.TaskDao
import com.nexaplanner.app.data.local.TaskEntity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject

@HiltViewModel
class DashboardViewModel @Inject constructor(
    private val taskDao: TaskDao
) : ViewModel() {
    val pendingTasks = taskDao.getPendingTasks().stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = emptyList()
    )

    fun toggleTaskStatus(task: TaskEntity) {
        viewModelScope.launch {
            if (task.status == 2) {
                // Revert to pending (simplified for demo)
            } else {
                taskDao.markAsDone(task.id)
            }
        }
    }
}
