package com.indie.search

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

data class SearchResult(val title: String, val url: String, val content: String)

class SearchAdapter(private var results: MutableList<SearchResult>) : 
    RecyclerView.Adapter<SearchAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val title: TextView = view.findViewById(R.id.resultTitle)
        val url: TextView = view.findViewById(R.id.resultUrl)
        val snippet: TextView = view.findViewById(R.id.resultSnippet)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = 
        ViewHolder(LayoutInflater.from(parent.context).inflate(R.layout.item_result, parent, false))

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = results[position]
        holder.title.text = item.title
        holder.url.text = item.url
        holder.snippet.text = if (item.content.length > 120) item.content.take(120) + "..." else item.content
    }

    override fun getItemCount() = results.size

    fun updateData(newResults: List<SearchResult>) {
        results.clear()
        results.addAll(newResults)
        notifyDataSetChanged()
    }
}
