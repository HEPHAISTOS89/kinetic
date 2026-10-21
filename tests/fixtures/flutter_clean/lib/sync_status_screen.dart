import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

// Regression fixture: diagnostics with emoji and tags are not UI copy,
// and IconButton.styleFrom is not an icon-only button.
class SyncStatusScreen extends StatelessWidget {
  const SyncStatusScreen({super.key, required this.onRetry});
  final VoidCallback onRetry;

  void _trace(String uri) {
    debugPrint(
      '🔗 [Router] Ignoring unsupported external URL: $uri',
    );
  }

  @override
  Widget build(BuildContext context) {
    _trace('x');
    return IconButton(
      tooltip: 'Retry sync',
      onPressed: onRetry,
      style: IconButton.styleFrom(minimumSize: const Size(48, 48)),
      icon: const Icon(Icons.refresh_outlined),
    );
  }
}
