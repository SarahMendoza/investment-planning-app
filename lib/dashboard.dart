// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'login_screen.dart';

// username() async {
//   SharedPreferences prefs = await SharedPreferences.getInstance();
//   String mail = prefs.getString('mail') ?? "";

//   return Text("Mail is: $mail");
// }

import 'dart:convert';
import 'package:http/http.dart' as http;

Future<List<Map<String, dynamic>>> fetchGoals(String userId) async {
  final response = await http.get(Uri.parse('http://localhost:5000/goals/$userId'));

  if (response.statusCode == 200) {
    final List data = json.decode(response.body);
    return data.map((goal) => goal as Map<String, dynamic>).toList();
  } else {
    throw Exception('Failed to load goals');
  }
}


class Dashboard extends StatefulWidget {
  const Dashboard({Key? key}) : super(key: key);

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  @override
  Widget build(BuildContext context) {

    List<Map<String, dynamic>> _goals = [];

    @override
    void initState() {
      super.initState();
      fetchGoals('user123').then((data) {
        setState(() {
          _goals = data;
        });
      });
    }


    return Scaffold(
      appBar: AppBar(
        title: const Text(''),
        centerTitle: true,
      ),
      body: Column(
        children: [
          // Title
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Text(
              'Dashboard',
              style: TextStyle(
                fontSize: 30,
              ),
            ),
          ),
          Expanded(
            child: Row(
              children: [
                // Left Section
                Expanded(
                  child: Column(
                    children: [ 
                      // const Padding(
                      //   padding: EdgeInsets.all(16.0),
                      //   child: Text.rich(
                      //     TextSpan(
                      //       text: "Goals",
                      //       style: TextStyle(
                      //         fontSize: 24,
                      //       ),
                      //     ),
                      //   ),
                      // ),
                      Expanded(
                        flex: 1,
                        child: Container(
                          width: 400,
                          child: SingleChildScrollView(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              children: List.generate(
                                20, // retrieve from number of goals
                                (index) => Container(
                                  width: double.infinity,
                                  child: Padding(
                                    padding: EdgeInsets.symmetric(vertical: 8.0),
                                    child: Card(
                                      child: Padding(
                                        padding: EdgeInsets.all(8.0),
                                        child: Row(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            SizedBox(
                                              width: 60,
                                              height: 60,
                                              child: Center(
                                                child: Stack(
                                                  alignment: Alignment.center,
                                                  children: [
                                                    CircularProgressIndicator(
                                                      value: 0.7, // completion value
                                                      strokeWidth: 6,
                                                    ),
                                                    Text(
                                                      '70%',
                                                      style: TextStyle(
                                                        fontSize: 10,
                                                      )
                                                    )
                                                  ],
                                                ),
                                              ),
                                            ),
                                            SizedBox(width: 16),

                                            Expanded(
                                              child: Column(
                                                crossAxisAlignment: CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                    'Goal', // specific goal
                                                    style: TextStyle(
                                                      fontSize: 18,
                                                      fontWeight: FontWeight.bold,
                                                    ),
                                                  ),
                                                  SizedBox(height: 4),
                                                  Text(
                                                    'Description of goal', // description of goal
                                                    style: TextStyle(
                                                      fontSize: 14,
                                                      color: Colors.grey,
                                                    ),
                                                  ),
                                                ],
                                              ),
                                            ),

                                            Center(
                                              child: IconButton(
                                                icon: Icon(Icons.more_vert),
                                                onPressed: () {
                                                  Navigator.push(context,
                                                  MaterialPageRoute(builder: (context) => Dashboard()));
                                                }, 
                                              ),
                                            ),
                                          ],
                                        ),
                                        // child: Text(
                                        //   'Left Section Item ${index + 1}',
                                        //   textAlign: TextAlign.center,
                                        // ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                // Right Section
                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Stock Portfolio
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Portfolio',
                                  style: TextStyle(
                                    fontSize: 20,
                                  ),
                                ),
                                // TO-DO: make this dynamic
                                const Divider(),
                                const Text('Thing 1'),
                                const Divider(),
                                const Text('Thing 2'),
                                const Divider(),
                                const Text('Thing 3'),
                              ]
                            )
                          )
                        ),
                        SizedBox(height: 16),
                        // Fixed Asset
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Fixed Assets',
                                  style: TextStyle(
                                    fontSize: 20,
                                  ),
                                ),
                                // TO-DO: make this dynamic
                                const Divider(),
                                _labeledItem('Property', '\$500,000'),
                                const Divider(),
                                _labeledItem('Property', '\$500,000'),
                                const Divider(),
                                _labeledItem('Property', '\$500,000'),
                              ],
                            ),
                          ),
                        ),
                        SizedBox(height: 16),
                        // Cash Investment
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Cash Investment',
                                  style: TextStyle(
                                    fontSize: 20,
                                  ),
                                ),
                                const Divider(),
                                _labeledItem('Thing 1', '\$15,000'),
                                const Divider(),
                                _labeledItem('Thing 2', '\$15,000'),
                                const Divider(),
                                _labeledItem('Thing 3', '\$15,500'),
                              ]
                            )
                          )
                        )
                      ]
                    )
                  )
                  // child: Container(
                  //   child: SingleChildScrollView(
                  //     padding: const EdgeInsets.all(16.0),
                  //     child: Column(
                  //       children: List.generate(
                  //         20,
                  //         (index) => Padding(
                  //           padding: const EdgeInsets.symmetric(vertical: 8.0),
                  //           child: Text('Right Section Item ${index + 1}'),
                  //         ),
                  //       ),
                  //     ),
                  //   ),
                  // ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

Widget _labeledItem(String label, String value) {
  return Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    children: [
      Text(label),
      Text(
        value,
        style: const TextStyle(fontWeight: FontWeight.bold),
      ),
    ],
  );
}
