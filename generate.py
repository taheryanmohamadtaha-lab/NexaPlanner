import os

def create_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"✅ Created: {path}")
# 1. Root Gradle Files
create_file("settings.gradle.kts", r"""
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://jitpack.io") }
    }
}
rootProject.name = "NexaPlanner"
include(":app")
""")

create_file("build.gradle.kts", r"""
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.20" apply false
    id("com.google.dagger.hilt.android") version "2.51.1" apply false
    id("com.google.devtools.ksp") version "2.0.20-1.0.24" apply false
}
""")

create_file("gradle.properties", r"""
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""")

create_file(".gitignore", r"""
*.iml
.gradle
/local.properties
/.idea/
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
""")

# 2. App Level Gradle
create_file("app/build.gradle.kts", r"""
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.dagger.hilt.android")
    id("com.google.devtools.ksp")
}

android {
    namespace = "com.nexaplanner.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.nexaplanner.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
        vectorDrawables { useSupportLibrary = true }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.10.00")
    implementation(composeBom)
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.6")
    implementation("androidx.activity:activity-compose:1.9.2")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    
    implementation("androidx.navigation:navigation-compose:2.8.2")
    implementation("com.google.dagger:hilt-android:2.51.1")
    ksp("com.google.dagger:hilt-compiler:2.51.1")
    implementation("androidx.hilt:hilt-navigation-compose:1.2.0")

    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")
    implementation("androidx.datastore:datastore-preferences:1.1.1")
    implementation("androidx.work:work-runtime-ktx:2.9.1")
    
    implementation("com.github.samanzamani:PersianDate:1.3.0")
    
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    debugImplementation("androidx.compose.ui:ui-tooling")
}
""")

# 3. Android Manifest
create_file("app/src/main/AndroidManifest.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />

    <application
        android:name=".NexaApplication"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="پلنر نکسا"
        android:supportsRtl="true"
        android:theme="@style/Theme.NexaPlanner"
        tools:targetApi="34">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.NexaPlanner">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

# 4. Resources
create_file("app/src/main/res/values/strings.xml", r"""<resources>
    <string name="app_name">پلنر نکسا</string>
</resources>
""")

create_file("app/src/main/res/values/themes.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.NexaPlanner" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
""")

create_file("app/src/main/res/drawable/ic_notification.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFF" android:pathData="M12,2C8.13,2 5,5.13 5,9c0,5.25 7,13 7,13s7,-7.75 7,-13c0,-3.87 -3.13,-7 -7,-7zM12,11.5c-1.38,0 -2.5,-1.12 -2.5,-2.5s1.12,-2.5 2.5,-2.5 2.5,1.12 2.5,2.5 -1.12,2.5 -2.5,2.5z"/>
</vector>
""")

# 5. Kotlin Source Files
create_file("app/src/main/java/com/nexaplanner/app/NexaApplication.kt", r"""package com.nexaplanner.app

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class NexaApplication : Application()
""")

create_file("app/src/main/java/com/nexaplanner/app/MainActivity.kt", r"""package com.nexaplanner.app

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.core.content.ContextCompat
import com.nexaplanner.app.ui.dashboard.DashboardScreen
import com.nexaplanner.app.ui.theme.NexaPlannerTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean -> }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                requestPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
        setContent {
            NexaPlannerTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    Scaffold { padding ->
                        DashboardScreen(modifier = Modifier.padding(padding))
                    }
                }
            }
        }
    }
}
""")

create_file("app/src/main/java/com/nexaplanner/app/data/local/TaskEntity.kt", r"""package com.nexaplanner.app.data.local

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
""")

create_file("app/src/main/java/com/nexaplanner/app/data/local/TaskDao.kt", r"""package com.nexaplanner.app.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface TaskDao {
    @Query("SELECT * FROM tasks ORDER BY isPinned DESC, startDate ASC")
    fun getAllTasks(): Flow<List<TaskEntity>>

    @Query("SELECT * FROM tasks WHERE status = 0 ORDER BY priority DESC, startDate ASC")
    fun getPendingTasks(): Flow<List<TaskEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTask(task: TaskEntity): Long

    @Query("UPDATE tasks SET status = 2 WHERE id = :taskId")
    suspend fun markAsDone(taskId: Int)
}
""")

create_file("app/src/main/java/com/nexaplanner/app/data/local/AppDatabase.kt", r"""package com.nexaplanner.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(entities = [TaskEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
}
""")

create_file("app/src/main/java/com/nexaplanner/app/core/di/DatabaseModule.kt", r"""package com.nexaplanner.app.core.di

import android.content.Context
import androidx.room.Room
import com.nexaplanner.app.data.local.AppDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(context, AppDatabase::class.java, "nexa_planner_db")
            .fallbackToDestructiveMigration()
            .build()
    }

    @Provides
    fun provideTaskDao(database: AppDatabase) = database.taskDao()
}
""")

create_file("app/src/main/java/com/nexaplanner/app/ui/theme/Theme.kt", r"""package com.nexaplanner.app.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF0061A4),
    secondary = Color(0xFF535F70),
    tertiary = Color(0xFF695776),
    background = Color(0xFFFDFCFF),
    surface = Color(0xFFFDFCFF),
    onPrimary = Color(0xFFFFFFFF),
    onBackground = Color(0xFF1A1C1E)
)

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF9ECAFF),
    secondary = Color(0xFFBBC7DB),
    tertiary = Color(0xFFD5BEE2),
    background = Color(0xFF1A1C1E),
    surface = Color(0xFF1A1C1E),
    onPrimary = Color(0xFF003258),
    onBackground = Color(0xFFE2E2E6)
)

@Composable
fun NexaPlannerTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.primary.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
""")

create_file("app/src/main/java/com/nexaplanner/app/ui/theme/Type.kt", r"""package com.nexaplanner.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)
""")

create_file("app/src/main/java/com/nexaplanner/app/ui/dashboard/DashboardViewModel.kt", r"""package com.nexaplanner.app.ui.dashboard

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
""")

create_file("app/src/main/java/com/nexaplanner/app/ui/dashboard/DashboardScreen.kt", r"""package com.nexaplanner.app.ui.dashboard

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.nexaplanner.app.data.local.TaskEntity
import ir.samanzamani.persiandate.PersianDate

@Composable
fun DashboardScreen(
    modifier: Modifier = Modifier,
    viewModel: DashboardViewModel = hiltViewModel()
) {
    val tasks by viewModel.pendingTasks.collectAsState()
    val currentDate = "${PersianDate().shYear}/${PersianDate().shMonth}/${PersianDate().shDay}"
    val completedCount = 0 // Simplified for demo
    val progress = 0.3f // Simplified for demo

    Scaffold(
        modifier = modifier,
        floatingActionButton = {
            FloatingActionButton(onClick = { /* Add Task Logic */ }, containerColor = MaterialTheme.colorScheme.primary) {
                Icon(Icons.Default.Add, contentDescription = "افزودن وظیفه")
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Text(text = "سلام، خوش آمدید! 👋", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                Text(text = "امروز: $currentDate", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("پیشرفت امروز", style = MaterialTheme.typography.titleMedium)
                        Spacer(modifier = Modifier.height(8.dp))
                        LinearProgressIndicator(
                            progress = { progress }, 
                            modifier = Modifier.fillMaxWidth().height(8.dp)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(text = "برای شروع، یک وظیفه جدید بسازید.", style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }

            item { Text("وظایف در انتظار", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }
            
            items(tasks) { task ->
                TaskItemCard(task = task, onToggleDone = { viewModel.toggleTaskStatus(task) })
            }
            
            if (tasks.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                        Text("هیچ وظیفه‌ای ثبت نشده است.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}

@Composable
fun TaskItemCard(task: TaskEntity, onToggleDone: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth(), elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)) {
        Row(modifier = Modifier.padding(16.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = task.status == 2, onCheckedChange = { onToggleDone() })
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(text = task.title, style = MaterialTheme.typography.titleMedium)
                Text(text = "اولویت: ${task.priority}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}
""")

# 6. GitHub Actions
create_file(".github/workflows/android-build.yml", r"""name: Android CI - Build Nexa Planner APK

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: gradle

    - name: Grant execute permission for gradlew
      run: chmod +x gradlew

    - name: Build Debug APK with Gradle
      run: ./gradlew assembleDebug --stacktrace

    - name: Upload Debug APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: NexaPlanner-Debug-APK
        path: app/build/outputs/apk/debug/app-debug.apk
        retention-days: 7
""")

# 7. Docs & README
create_file("docs/RESEARCH.md", r"""# سند تحقیق و معماری فنی - Nexa Planner
- **زبان:** Kotlin 2.0.20
- **UI:** Jetpack Compose + Material 3
- **معماری:** MVVM + Hilt + Room
- **تاریخ شمسی:** PersianDate (JitPack)
- **CI/CD:** GitHub Actions (Ubuntu, JDK 17, Gradle 8.5)
""")

create_file("README.md", r"""# 📱 پلنر نکسا (Nexa Planner)

اپلیکیشن برنامه‌ریزی حرفه‌ای اندروید با Jetpack Compose.

## 🚀 دریافت APK
۱. به تب **Actions** در گیت‌هاب بروید.
۲. روی **Android CI - Build Nexa Planner APK** کلیک کنید.
۳. دکمه **Run workflow** را بزنید.
۴. پس از اتمام، فایل `NexaPlanner-Debug-APK` را از بخش **Artifacts** دانلود کنید.

## 🛠️ اجرای محلی
پروژه را در Android Studio باز کرده و دکمه Run را بزنید.
""")

print("\n🎉 پروژه نکسا پلنر با موفقیت ساخته شد!")
print("📁 اکنون می‌توانید این پوشه را در GitHub آپلود کنید.")