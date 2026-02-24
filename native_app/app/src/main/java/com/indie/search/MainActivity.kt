package com.indie.search

import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import com.google.android.material.bottomsheet.BottomSheetDialog

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val accountBtn = findViewById<ImageView>(R.id.btnAccount)
        val searchCard = findViewById<CardView>(R.id.homeSearchCard)

        // 1. Account Button Click -> Show SSO/Settings Drawer
        accountBtn.setOnClickListener {
            val dialog = BottomSheetDialog(this)
            val view = layoutInflater.inflate(R.layout.account_sheet, null)
            dialog.setContentView(view)
            dialog.show()
        }

        // 2. Search Bar Click -> Go to Search Activity
        searchCard.setOnClickListener {
            val intent = Intent(this, SearchActivity::class.java)
            startActivity(intent)
        }
    }
}

