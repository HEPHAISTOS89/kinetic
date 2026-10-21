import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return MediaQuery(
      data: MediaQuery.of(context).copyWith(textScaler: TextScaler.noScaling),
      child: Scaffold(
        floatingActionButton: FloatingActionButton(onPressed: () {}, child: const Icon(Icons.add)),
        body: Container(
          width: 375,
          decoration: const BoxDecoration(
            gradient: LinearGradient(colors: [Color(0xFF7C3AED), Color(0xFFDB2777)]),
          ),
          child: ListView(
            padding: const EdgeInsets.all(13),
            children: [
              const Text('Good morning, Sam 👋', style: TextStyle(fontSize: 28, color: Colors.white)),
              const SizedBox(height: 17),
              const Text('Unlock your potential with seamless insights', style: TextStyle(fontSize: 15, color: Color(0xFFE5E7EB))),
              const SizedBox(height: 23),
              Card(
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
                child: const Padding(padding: EdgeInsets.all(14), child: Text('4.9★ from 10k+ users', style: TextStyle(fontSize: 13))),
              ).animate().fadeIn().slideY(),
              Card(
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                child: Row(children: [
                  IconButton(icon: const Icon(Icons.favorite_outline), onPressed: () {}),
                  IconButton(icon: const Icon(Icons.share_rounded), onPressed: () {}, materialTapTargetSize: MaterialTapTargetSize.shrinkWrap),
                  const Icon(Icons.star),
                  const FittedBox(child: Text('Your weekly streak 🔥', style: TextStyle(fontSize: 11))),
                ]),
              ).animate().fadeIn(delay: 100.ms).slideY(),
              Card(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)), child: const Text('Stats', style: TextStyle(fontSize: 19))).animate().fadeIn(delay: 200.ms).slideY(),
              Card(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)), child: const Text('More', style: TextStyle(fontSize: 21, color: Color(0xFF6B7280)))).animate().fadeIn(delay: 300.ms),
              Card(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)), child: const Text('Tips', textAlign: TextAlign.center, style: TextStyle(fontSize: 17, color: Color(0xFF9CA3AF)))),
              const Text('Another', style: TextStyle(fontSize: 22, color: Color(0xFF4B5563))),
              const Text('x', style: TextStyle(fontSize: 26, color: Color(0xFF374151))),
              const Text('y', style: TextStyle(fontSize: 34, color: Color(0xFF1F2937))),
              const Text('z', style: TextStyle(fontSize: 12, color: Color(0xFFD1D5DB))),
              const Text('w', style: TextStyle(fontSize: 10, color: Color(0xFF111827))),
              TweenAnimationBuilder<double>(tween: Tween(begin: 0, end: 1), duration: const Duration(milliseconds: 900), curve: Curves.elasticOut, builder: (c, v, _) => Opacity(opacity: v, child: const SizedBox())),
            ],
          ),
        ),
      ),
    );
  }
}
