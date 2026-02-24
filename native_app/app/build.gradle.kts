plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.indie.search" 
    compileSdk = 34

    defaultConfig {
        applicationId = "com.indie.search"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    // Isse errors ignore honge aur build rukega nahi
    lint {
        checkReleaseBuilds = false
        abortOnError = false
        checkDependencies = false
    }

    // Resources handling fix
    aaptOptions {
        noCompress("png")
    }
}

dependencies {
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.9.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
}
