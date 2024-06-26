package com.lzb.utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;

public class TextFileUtil {

	public static String read(String filePath, String encoding) {

		File file = new File(filePath);
		if (!file.exists()) {
			System.out.println("文件不存在");
			System.exit(-1);
		}

		FileInputStream fis = null;
		InputStreamReader isr = null;
		StringBuilder fileContent = new StringBuilder();

		try {
			fis = new FileInputStream(file);
			isr = new InputStreamReader(fis, encoding);
			BufferedReader br = new BufferedReader(isr);
			String line = null;
			while ((line = br.readLine()) != null) {
				fileContent.append(line).append("\n");
			}
			fileContent.deleteCharAt(fileContent.length() - 1);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				isr.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return fileContent.toString();
	}
}
