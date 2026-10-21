import 'package:flutter/material.dart';
import 'theme/tokens.dart';

class TonightScreen extends StatelessWidget {
  const TonightScreen({super.key, required this.minutes, required this.onLog});
  final int? minutes;
  final VoidCallback onLog;

  @override
  Widget build(BuildContext context) {
    final type = Theme.of(context).textTheme;
    final reduce = MediaQuery.disableAnimationsOf(context);
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: KSpace.xl),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Spacer(),
            AnimatedSwitcher(
              duration: reduce ? Duration.zero : const Duration(milliseconds: 220),
              child: minutes == null
                  ? Text('Your first night appears here tomorrow.', style: type.bodyLarge)
                  : Text('${minutes! ~/ 60} h ${minutes! % 60}', style: type.displaySmall),
            ),
            const SizedBox(height: KSpace.s),
            Text('A little shorter than your week.', style: type.bodyLarge),
            const SizedBox(height: KSpace.xl),
            IconButton(tooltip: 'Log a wake-up', icon: const Icon(Icons.edit_outlined), onPressed: onLog),
            const SizedBox(height: KSpace.l),
          ]),
        ),
      ),
    );
  }
}
