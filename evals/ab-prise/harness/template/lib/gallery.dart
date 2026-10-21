import 'package:flutter/material.dart';

/// Every state you designed, rendered by test/render_test.dart.
/// Each builder returns the WHOLE app for that state (MaterialApp/WidgetsApp + theme)
/// in the given brightness. Use short kebab-case names.
typedef GalleryEntry = (String name, Widget Function(Brightness brightness) build);

List<GalleryEntry> get gallery => [
      ('placeholder', (b) => MaterialApp(
            debugShowCheckedModeBanner: false,
            theme: ThemeData(brightness: b),
            home: const Scaffold(body: Center(child: Text('Replace me'))),
          )),
    ];
