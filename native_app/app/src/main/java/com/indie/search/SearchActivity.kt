package com.indie.search

import android.os.Bundle
import android.view.inputmethod.EditorInfo
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import okhttp3.*
import org.json.JSONArray
import java.io.IOException

class SearchActivity : AppCompatActivity() {

    private lateinit var adapter: SearchAdapter
    private val client = OkHttpClient()
    
    // Aapki Supabase Details maine yahan daal di hain
    private val supabaseUrl = "https://jhyqyskemsvoizmmupka.supabase.co/rest/v1/pages"
    private val supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpoeXF5c2tlbXN2b2l6bW11cGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4NDQ5ODUsImV4cCI6MjA4NzQyMDk4NX0.IvjAWJZ4DeOCNG0SzKgV5P-LXW2aYvX_RA-NDw5S-ec"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search)

        val recyclerView = findViewById<RecyclerView>(R.id.resultsRecyclerView)
        val searchBar = findViewById<EditText>(R.id.searchEditText)

        adapter = SearchAdapter(mutableListOf())
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        searchBar.setOnEditorActionListener { v, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                fetchResults(v.text.toString())
                true
            } else false
        }
    }

    private fun fetchResults(query: String) {
        val url = "$supabaseUrl?content=ilike.*$query*&select=title,url,content"
        val request = Request.Builder()
            .url(url)
            .addHeader("apikey", supabaseKey)
            .addHeader("Authorization", "Bearer $supabaseKey")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) { e.printStackTrace() }
            override fun onResponse(call: Call, response: Response) {
                val data = response.body?.string()
                if (data != null) {
                    val jsonArray = JSONArray(data)
                    val results = mutableListOf<SearchResult>()
                    for (i in 0 until jsonArray.length()) {
                        val obj = jsonArray.getJSONObject(i)
                        results.add(SearchResult(
                            obj.optString("title", "No Title"),
                            obj.optString("url", "#"),
                            obj.optString("content", "")
                        ))
                    }
                    runOnUiThread { adapter.updateData(results) }
                }
            }
        })
    }
}
