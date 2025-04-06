import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:web_socket_channel/io.dart';

import 'create_account.dart';
import 'dashboard.dart';


import 'package:http/http.dart' as http;

void login(String username, String password, BuildContext context) async {
  final response = await http.post(
    Uri.parse('http://127.0.0.1:5000/user/login'), // Use your backend IP if on device
    headers: {"Content-Type": "application/json"},
    body: json.encode({
      "username": username,
      "password": password,
    }),
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_name', data['user_name']);
    Navigator.push(context, MaterialPageRoute(builder: (_) => Dashboard()));
  } else {
    final message = json.decode(response.body)['message'];
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text("Login Failed"),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text("OK"),
          )
        ],
      ),
    );
  }
}




class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  @override
  Widget build(BuildContext context) {
    String _user = "";
    String _pwd = "";

    return Scaffold(
      appBar: AppBar(
        title: const Text(''),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 64.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text.rich(
                TextSpan(
                  text: "Our Platform Name",
                  style: TextStyle(
                    fontSize: 30,
                  ),
                ),
              ),
              const SizedBox(height: 32),
              // const Card(
              //   child: ListTile(
              //     title: Text("Our Platform Name"),
              //   )
              // ),
              TextField(
                onChanged: (val) => _user = val,
                decoration: InputDecoration(
                  labelText: 'Username',
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                obscureText: true,
                onChanged: (val) => _pwd = val,
                decoration: InputDecoration(
                  labelText: 'Password',
                ),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  TextButton(
                    onPressed: () {
                    
                    },
                    child: const Text('Forgot Password'),
                  ),
                ],
              ),
              const SizedBox(height: 64),
              SizedBox(
                width: 200,
                child: OutlinedButton(
                  onPressed: () {
                    // Navigator.push(context,
                    // MaterialPageRoute(builder: (context) => Dashboard()));
                    login(_user, _pwd, context);
                  },
                  child: const Text('Login'),
                ),
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: 200,
                child: OutlinedButton(
                  onPressed: () {
                    Navigator.push(context,
                    MaterialPageRoute(builder: (context) => CreateAccount()));
                  },
                  child: const Text('Create Account'),
                ),
              ),
              // Row(
              //   mainAxisAlignment: MainAxisAlignment.center,
              //   children: [
              //     TextButton(
              //       onPressed: () {},
              //       child: const Text('Forgot Password'),
              //     ),
              //     TextButton(
              //       onPressed: () {},
              //       child: const Text('Create Account'),
              //     ),
              //   ],
              // ),
            ],
          ),
        ),
      ),
    );
  }
}