package com.lzb;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.regex.Pattern;

import com.lzb.utils.TextFileUtil;

public class Client {

	public static void main(String[] args) {

		String encoding = "GBK";
		String fileEncoding = "UTF-8";
		String addr = null;
		String filePath = "client.txt";

		// 读取参数
		if (args != null && args.length > 0) {
			for (int i = 0; i < args.length; i++) {
				// 帮助
				if ("-h".equals(args[i]) || "--help".equals(args[i]) || "-help".equals(args[i])) {
					printHelp();
					return;
				}
				if ("-a".equals(args[i])) {
					checkNext(args, i);
					addr = args[i + 1];
					if (!addr.contains(":") || !isNumeric(addr.split(":")[1])) {
						System.out.println("-a参数值不正确");
						printHelp();
						return;
					}
				} else if ("-f".equals(args[i])) {
					checkNext(args, i);
					filePath = args[i + 1];
				} else if ("-c".equals(args[i])) {
					checkNext(args, i);
					encoding = args[i + 1];
				} else if ("-fc".equals(args[i])) {
					checkNext(args, i);
					fileEncoding = args[i + 1];
				}
			}
		}

		// 检查必须参数
		if (isEmpty(addr)) {
			System.out.println("缺少参数-a");
			printHelp();
			return;
		}

		String content = TextFileUtil.read(filePath, fileEncoding);
		send(addr, content, encoding);

	}

	private static void printHelp() {

		System.out.println("使用示例: java -jar client.jar -a 127.0.0.1:18188");
		System.out.println("        java -jar client.jar -a 127.0.0.1:18188 -c GBK -f ./abc.txt -fc UTF-8");
		System.out.println("参数:");
		System.out.println("	-a 必须,服务端的ip和端口号");
		System.out.println("	-c 可选,与服务端交互的字符编码，默认为GBK");
		System.out.println("	-f 可选,存放报文的文本文件,默认值为./client.txt");
		System.out.println("	-fc 可选,存放报文的文本文件的字符编码，默认为UTF-8");
	}

	private static boolean isEmpty(String addr) {

		if (addr == null || addr.length() < 1) {
			return true;
		}
		return false;
	}

	public static boolean isNumeric(String str) {

		if (isEmpty(str)) {
			return false;
		}
		Pattern pattern = Pattern.compile("[0-9]*");
		return pattern.matcher(str).matches();
	}

	private static void checkNext(String[] args, int i) {

		if (args.length - 1 < i + 1) {
			System.out.println("参数格式不正确");
			printHelp();
			System.exit(0);
		}
	}

	private static void send(String addr, String content, String encoding) {

		String[] split = addr.split(":");
		String host = split[0];
		String port = split[1];
		Socket socket = null;
		OutputStream os = null;
		BufferedReader br = null;
		try {
			// 客户端socket
			System.out.println("客户端启动,目标地址:"+addr);
			socket = new Socket(host, Integer.parseInt(port));
			// 请求内容
			os = socket.getOutputStream();
			System.out.println("发送请求报文:\n" + content);
			os.write(content.getBytes(encoding));
			os.flush();

			socket.shutdownOutput();

			// 获取响应
			br = new BufferedReader(new InputStreamReader(socket.getInputStream(), encoding));
			String reply = null;
			while ((reply = br.readLine()) != null) {
				System.out.println("接收到响应报文:\n" + reply);
			}

		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			try {
				br.close();
				os.close();
				socket.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

}
