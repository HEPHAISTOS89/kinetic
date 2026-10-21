package app.ui

import androidx.compose.runtime.Composable
import androidx.compose.material3.*

@Composable
fun HomeScreen() {
    Column(Modifier.padding(13.dp).background(Brush.verticalGradient(listOf(Color(0xFF7C3AED), Color(0xFFEC4899))))) {
        Text("Welcome back, Sam!", fontSize = 27.sp, textAlign = TextAlign.Center)
        IconButton(onClick = { }) { Icon(Icons.Filled.Favorite, contentDescription = null) }
        Box(Modifier.size(32.dp).clickable { })
        Card(shape = RoundedCornerShape(17.dp)) { Text("Elevate your workflow", fontSize = 13.sp, maxLines = 1, overflow = TextOverflow.Ellipsis) }
        Icon(Icons.Outlined.Share, contentDescription = "Share")
        val a by animateFloatAsState(1f, animationSpec = spring(dampingRatio = Spring.DampingRatioHighBouncy))
        Spacer(Modifier.height(23.dp))
    }
}
