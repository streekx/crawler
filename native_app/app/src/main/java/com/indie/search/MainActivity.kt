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

        findViewById<CardView>(R.id.homeSearchCard).setOnClickListener {
            startActivity(Intent(this, SearchActivity::class.java))
        }

        findViewById<ImageView>(R.id.btnAccount).setOnClickListener {
            val dialog = BottomSheetDialog(this)
            dialog.setContentView(layoutInflater.inflate(R.layout.account_sheet, null))
            dialog.show()
        }
    }
}
