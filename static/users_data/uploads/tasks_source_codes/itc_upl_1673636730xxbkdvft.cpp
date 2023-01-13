#include "middle_str.h"
#include "binary.h"
#include <iostream>

using namespace std;

string itc_covert_num(int number, int ss)
{
	string otv1 = "", otv2 = "";
	if ((ss > 16) || (ss < 2) || (number < 0))
		return "-1";
	
	else if (ss < 10) {
		while (number > 0) {
			otv1 += ('0' + (number % ss));
			number /= ss;
		}
	}
	else {
		while (number > 0) {
			if (number % ss >= 10) otv1 += ('A' + (number % ss) - 10);
			else otv1 += ('0' + (number % ss));
			number /= ss;
		}
	}
	int i = itc_len(otv1);
	while (i > 0) {
		i--;
		otv2 += otv1[i];
	}
	return otv2;
}

string itc_num_to_str(long long num){
    char ch = ' ';
    string str = "";
    while(num > 0){
        ch = (num % 10) + 48;
        str =  ch + str;
        num /= 10;
    }
    return str;
}

long long str_to_num(string temp){
    int ch = 0;
    long long temp_num = 0;
    for (long long i = 0; temp[i] != '\0'; ++i){
        ch = temp[i] - 48;
        temp_num = temp_num * 10 + ch;
    }
    return temp_num;
}
