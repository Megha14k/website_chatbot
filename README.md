# Website Chatbot using Ollama

A Python-based chatbot that scrapes a website and answers questions using a local LLM (Ollama).

## About

This project scrapes any public website and uses the **Ollama LLaMA-2 model** to answer user questions based only on the site’s content.

## Features

- No external API calls — all LLM inference runs locally
- Automatically scrapes and chunks website text
- Short, simple, deterministic responses
- Easy CLI chatbot

## Requirements

Install dependencies:

```bash
pip install requests beautifulsoup4

## Install Ollama

### Windows
1. Go to: https://ollama.com
2. Download the Windows installer
3. Run the installer and complete setup
4. Restart your system if required

Verify installation:
```bash
ollama --version
