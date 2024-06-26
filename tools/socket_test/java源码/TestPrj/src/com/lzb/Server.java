package com.lzb;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.regex.Pattern;

public class Server {

	public static void main(String[] args) {
		String encoding = "GBK";
		String fileEncoding = "UTF-8";
		String port = null;
		String filePath = "server.txt";
		
		//读取参数
		if(args!=null && args.length>0){
			for(int i=0;i<args.length;i++){
				//帮助
				if("-h".equals(args[i]) || "--help".equals(args[i]) || "-help".equals(args[i])){
					printHelp();
					return;
				}
				if("-p".equals(args[i])){
					checkNext(args,i);
					port = args[i+1];
					if(!isNumeric(port)){
						System.out.println("-p参数值不正确");
						printHelp();
						return;
					}
				}else if("-f".equals(args[i])){
					checkNext(args,i);
					filePath = args[i+1];
				}else if("-c".equals(args[i])){
					checkNext(args,i);
					encoding = args[i+1];
				}else if("-fc".equals(args[i])){
					checkNext(args,i);
					fileEncoding = args[i+1];
				}
			}
		}
		
		//检查必须参数
		if(isEmpty(port)){
			System.out.println("缺少参数-p");
			printHelp();
			return;
		}
		
		startServer(port,encoding,filePath,fileEncoding);
		
	}
	
	private static void printHelp(){
		System.out.println("使用示例: java -jar server.jar -p 10194");
		System.out.println("        java -jar server.jar -p 10194 -c GBK -f ./abc.txt -fc UTF-8");
		System.out.println("参数:");
		System.out.println("	-p 必须,服务端的端口号");
		System.out.println("	-c 可选,与客户端交互的字符编码，默认为GBK");
		System.out.println("	-f 可选,存放响应报文的文本文件,默认值为./server.txt");
		System.out.println("	-fc 可选,存放响应报文的文本文件的字符编码，默认为UTF-8");
	}
	
	private static void startServer(String port,String encoding, String filePath, String fileEncoding) {
		ServerSocket serverSocket = null;
		Socket socket = null;
		
		try {
			//创建Socket，指定端口号
			System.out.println("服务器启动,端口:"+port);
			serverSocket = new ServerSocket(Integer.parseInt(port));
			while(true){
				//accept接收
				socket = serverSocket.accept();
				System.out.println("接收到请求");
				new ServerThread(socket,encoding,filePath,fileEncoding).start();
			}
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			try {
				//关闭流
				if(serverSocket!=null){
					serverSocket.close();
				}
				
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
	}
	
	private static boolean isEmpty(String addr) {
		if(addr==null || addr.length()<1){
			return true;
		}
		return false;
	}
	
	public static boolean isNumeric(String str){
		if(isEmpty(str)){
			return false;
		}
	    Pattern pattern = Pattern.compile("[0-9]*");
	    return pattern.matcher(str).matches();   
	}

	private static void checkNext(String[] args, int i) {
		if(args.length-1<i+1){
			System.out.println("参数格式不正确");
			printHelp();
			System.exit(0);
		}
	}
	
}
