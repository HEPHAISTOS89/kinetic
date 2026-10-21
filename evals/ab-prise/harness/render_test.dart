// Render harness — do not modify. Renders every gallery entry at 393×852 logical px
// (device pixel ratio 2) with iPhone-like safe-area insets (top 47, bottom 34), light and dark, into ../shots/<name>-<light|dark>.png.
// Run: flutter test --update-goldens test/render_test.dart
import 'dart:convert';
import 'dart:io';

import 'package:app/gallery.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

Future<void> _loadFamily(String family, Iterable<String> files) async {
  final loader = FontLoader(family);
  for (final f in files) {
    final bytes = File(f).readAsBytesSync();
    loader.addFont(Future.value(ByteData.view(bytes.buffer)));
  }
  await loader.load();
}

Future<void> _loadFonts() async {
  // Roboto + Material Icons from the Flutter SDK cache. Roboto also stands in for the
  // iOS system font (SF is not available to the test renderer).
  var dir = File(Platform.resolvedExecutable).parent;
  while (!Directory('${dir.path}/material_fonts').existsSync() && dir.path != dir.parent.path) {
    dir = dir.parent;
  }
  final mf = '${dir.path}/material_fonts';
  final roboto = Directory(mf).listSync().map((e) => e.path)
      .where((p) => p.contains('Roboto-') && p.endsWith('.ttf')).toList();
  for (final fam in ['Roboto', 'CupertinoSystemText', 'CupertinoSystemDisplay',
      '.SF Pro Text', '.SF Pro Display', '.SF UI Text', '.SF UI Display']) {
    await _loadFamily(fam, roboto);
  }
  await _loadFamily('MaterialIcons', ['$mf/MaterialIcons-Regular.otf']);
  // Every family declared in pubspec (app fonts and packages such as cupertino_icons).
  final manifest = json.decode(await rootBundle.loadString('FontManifest.json')) as List;
  for (final fam in manifest) {
    final loader = FontLoader(fam['family'] as String);
    for (final font in fam['fonts'] as List) {
      loader.addFont(rootBundle.load(font['asset'] as String));
    }
    await loader.load();
  }
}

void main() {
  setUpAll(_loadFonts);
  for (final (name, build) in gallery) {
    for (final b in Brightness.values) {
      final suffix = b == Brightness.light ? 'light' : 'dark';
      testWidgets('$name-$suffix', (tester) async {
        tester.view.physicalSize = const Size(393 * 2, 852 * 2);
        tester.view.devicePixelRatio = 2;
        tester.view.padding = const FakeViewPadding(top: 47 * 2, bottom: 34 * 2);
        tester.view.viewPadding = const FakeViewPadding(top: 47 * 2, bottom: 34 * 2);
        tester.platformDispatcher.platformBrightnessTestValue = b;
        addTearDown(tester.view.reset);
        addTearDown(tester.platformDispatcher.clearAllTestValues);
        const key = ValueKey('kinetic-render-root');
        await tester.pumpWidget(RepaintBoundary(key: key, child: build(b)));
        await tester.pump(const Duration(seconds: 2));
        await expectLater(find.byKey(key), matchesGoldenFile('../shots/$name-$suffix.png'));
      });
    }
  }
}
