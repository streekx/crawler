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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search)

        val recyclerView = findViewById<RecyclerView>(R.id.resultsRecyclerView)
        val searchBar = findViewById<EditText>(R.id.searchEditText)

        adapter = SearchAdapter(mutableListOf())
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        // Get query from intent (Coming from Home Screen)
        val initialQuery = intent.getStringExtra("query")
        if (initialQuery != null) {
            searchBar.setText(initialQuery)
            fetchResults(initialQuery)
        }

        // Handle search from bottom bar
        searchBar.setOnEditorActionListener { v, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                fetchResults(v.text.toString())
                true
            } else false
        }
    }

    private fun fetchResults(query: String) {
        val url = "YOUR_SUPABASE_URL/rest/v1/pages?content=ilike.*$query*&select=title,url,content"
        val request = Request.Builder()
            .url(url)
            .addHeader("apikey", "YOUR_ANON_KEY")
            .addHeader("Authorization", "Bearer YOUR_ANON_KEY")
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
                            obj.getString("title"),
                            obj.getString("url"),
                            obj.getString("content")
                        ))
                    }
                    runOnUiThread { adapter.updateData(results) }
                }
            }
        })
    }
}

