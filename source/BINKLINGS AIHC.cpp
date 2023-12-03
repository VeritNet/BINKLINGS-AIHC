#include <stdio.h>
#include <stdlib.h>
#include "httplib.h"
#include <iostream>
#include <string>
#include <windows.h>
#include <fstream>

using namespace std;

void doGet(const httplib::Request& req, httplib::Response& res) {
    int result = WinExec(".\\program\\HC.exe", SW_HIDE);
    if (result > 31) {
        res.set_content("Started", "text/plain");
        ShowWindow(GetConsoleWindow(), SW_SHOW);
    } else {
        res.set_content("Err: " + to_string(result), "text/plain");
    }
}

void noCon(const httplib::Request& req, httplib::Response& res) {
    int result = WinExec(".\\program\\HC.exe", SW_HIDE);
    ShowWindow(GetConsoleWindow(), SW_HIDE);
    if (result > 31) {
        res.set_content("Started", "text/plain");
    }
    else {
        res.set_content("Err: " + to_string(result), "text/plain");
    }
}

void stop(const httplib::Request& req, httplib::Response& res) {
    int result = WinExec("taskkill /f /im HC.exe", SW_HIDE);
    if (result > 31) {
        res.set_content("stopped", "text/plain");
        ShowWindow(GetConsoleWindow(), SW_SHOW);
    } else {
        res.set_content("Err: " + to_string(result), "text/plain");
    }
}

void ep(const httplib::Request& req, httplib::Response& res) {
    int result = WinExec("taskkill /f /im HC.exe", SW_HIDE);
    if (result > 31) {
        res.set_content("end", "text/plain");
        exit(0);
    } else {
        res.set_content("Err: " + to_string(result), "text/plain");
    }
}

std::string read(std::string path) {
    std::ifstream file(path);
    std::string content;
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            content += line + "\n";
        }
        file.close();
    }
    return content;
}

void returnHtml(const httplib::Request& req, httplib::Response& res)
{
    res.set_header("Access-Control-Allow-Origin", "*");
    std::string html = read("./GUI/index.html");
    res.set_content(html, "text/html");
}

void returnCss(const httplib::Request& req, httplib::Response& res)
{
    res.set_header("Access-Control-Allow-Origin", "*");
    std::string html = read("./GUI/material.cyan-light_blue.min.css");
    res.set_content(html, "text/plane");
}

int main(int argc, char* argv[])
{
    httplib::Server server;
    WinExec(".\\start.bat", SW_HIDE);
    server.Get("/start", doGet);
    server.Get("/nc", noCon);
    server.Get("/", returnHtml);
    server.Get("/css", returnCss);
    server.Get("/stop", stop);
    server.Get("/end", ep);
    server.listen("0.0.0.0", 5726);
    return 0;
}