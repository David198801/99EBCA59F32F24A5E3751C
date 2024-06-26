package com.lzb;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.Socket;

import com.lzb.utils.TextFileUtil;

public class ServerThread extends Thread {

	private Socket socket;
	private String filePath;
	private String encoding;
	private String fileEncoding;

	public ServerThread(Socket socket, String encoding, String filePath, String fileEncoding) {

		this.socket = socket;
		this.encoding = encoding;
		this.filePath = filePath;
		this.fileEncoding = fileEncoding;
	}

	@Override
	public void run() {

		BufferedReader br = null;
		BufferedWriter wr = null;

		try {
			// 获得用户请求
			System.out.println("响应线程" + Thread.currentThread().getName() + "启动");
			br = new BufferedReader(new InputStreamReader(socket.getInputStream(), encoding));

			StringBuilder sb = new StringBuilder();
			String line = null;
			while ((line = br.readLine()) != null) {
				sb.append(line).append("\n");
			}
			sb.deleteCharAt(sb.length() - 1);
			System.out.println("请求报文:\n" + sb.toString());
			InetAddress ia = socket.getInetAddress();
			System.out.println("客户端IP地址:" + ia.getHostAddress());

			// 响应客户端
			wr = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), encoding));
			// 响应内容
			String reply = TextFileUtil.read(filePath, fileEncoding);
			System.out.println("发送响应报文:\n" + reply);
			// 写入输出流发送
			wr.write(reply);

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			try {
				// 关闭流
				if (wr != null) {
					wr.close();
				}
				if (br != null) {
					br.close();
				}
				if (socket != null) {
					socket.close();
				}
				System.out.println("响应线程" + Thread.currentThread().getName() + "结束");

			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
	}

}