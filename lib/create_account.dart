// ignore_for_file: prefer_const_constructors

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:web_socket_channel/io.dart';
import 'package:flutter/services.dart';

import 'survey.dart';
import 'login_screen.dart';

// signUp(context, _mail, _user, _pwd, _cpwd) async {
//   // Check if email is valid.
//   bool isValid = RegExp(
//           r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+")
//       .hasMatch(_mail);
//   String auth = "chatappauthkey231r4";
//   // Check if email is valid
//   if (isValid == true) {
//     if (_pwd == _cpwd) {
//       IOWebSocketChannel channel;
//       try {
//         // Create connection.
//         channel = IOWebSocketChannel.connect('http://127.0.0.1:5000/');
//       } catch (e) {
//         print("Error on connecting to websocket: " + e);
//       }
//       // Data that will be sended to Node.js
//       String signUpData =
//           "{'auth':'$auth','cmd':'signup','email':'$_mail','username':'$_user','hash':'$_cpwd'}";
//       // Send data to Node.js
//       channel.sink.add(signUpData);
//       // listen for data from the server
//       channel.stream.listen((event) async {
//         event = event.replaceAll(RegExp("'"), '"');
//         var signupData = json.decode(event);
//         // Check if the status is succesfull
//         if (signupData["status"] == 'succes') {
//           // Close connection.
//           channel.sink.close();
//           // Return user to login if succesfull
//           return Navigator.push(
//             context,
//             MaterialPageRoute(builder: (context) => LoginScreen()),
//           );
//         } else {
//           channel.sink.close();
//           print("Error signing signing up");
//         }
//       });
//     } else {
//       print("Password are not equal");
//     }
//   } else {
//     print("email is false");
//   }
// }

class CreateAccount extends StatefulWidget {
  const CreateAccount({Key? key}) : super(key: key);

  @override
  State<CreateAccount> createState() => _CreateAccountState();
}

class _CreateAccountState extends State<CreateAccount> {
  @override
  Widget build(BuildContext context) {
    // String _firstname;
    // String _lastname;
    // String _birthdate:
    // String _mail;
    // String _user;
    // String _pwd;
    // String _cpwd;


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
                  text: "Create Account",
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
                textCapitalization: TextCapitalization.words,
                decoration: InputDecoration(
                  labelText: 'First name',
                ),
              ),
              const SizedBox(height: 8),
              TextField(
                textCapitalization: TextCapitalization.words,
                decoration: InputDecoration(
                  labelText: 'Last name',
                ),
              ),
              const SizedBox(height: 8),
              const TextField(
                decoration: InputDecoration(
                  labelText: 'Birthdate (mm-dd-yyyy)',
                ),
              ),
              const SizedBox(height: 8),
              const TextField(
                keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                  labelText: 'Email address',
                ),
              ),
              const SizedBox(height: 8),
              const TextField(
                decoration: InputDecoration(
                  labelText: 'Username',
                ),
              ),
              const SizedBox(height: 8),
              const TextField(
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                ),
              ),
              const SizedBox(height: 8),
              const TextField(
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Confirm password',
                ),
              ),
              const SizedBox(height: 64),
              SizedBox(
                width: 200,
                child: OutlinedButton(
                  onPressed: () {
                    // Navigator.push(context,
                    // MaterialPageRoute(builder: (context) => Survey()));
                  },
                  child: const Text('Continue'),
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
