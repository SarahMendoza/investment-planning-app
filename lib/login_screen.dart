import 'package:flutter/material.dart';
import 'create_account.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
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
              const TextField(
                decoration: InputDecoration(
                  labelText: 'Username',
                ),
              ),
              const SizedBox(height: 16),
              const TextField(
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                ),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  TextButton(
                    onPressed: () {
                      Navigator.push(context,
                      MaterialPageRoute(builder: (context) => CreateAccount()));
                    },
                    child: const Text('Forgot Password'),
                  ),
                ],
              ),
              const SizedBox(height: 64),
              SizedBox(
                width: 200,
                child: OutlinedButton(
                  onPressed: () {},
                  child: const Text('Login'),
                ),
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: 200,
                child: OutlinedButton(
                  onPressed: () {},
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