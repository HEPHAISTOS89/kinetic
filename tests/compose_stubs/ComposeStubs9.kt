@file:Suppress("unused", "UNUSED_PARAMETER")
package androidx.compose.material3
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
private val U = Color(0L)
private val T = TextStyle()
class ColorScheme
fun lightColorScheme(primary: Color = U, onPrimary: Color = U, background: Color = U, onBackground: Color = U,
                     surface: Color = U, onSurface: Color = U, onSurfaceVariant: Color = U, outline: Color = U,
                     outlineVariant: Color = U, error: Color = U): ColorScheme = ColorScheme()
fun darkColorScheme(primary: Color = U, onPrimary: Color = U, background: Color = U, onBackground: Color = U,
                    surface: Color = U, onSurface: Color = U, onSurfaceVariant: Color = U, outline: Color = U,
                    outlineVariant: Color = U, error: Color = U): ColorScheme = ColorScheme()
class Typography(val displayLarge: TextStyle = T, val displayMedium: TextStyle = T, val displaySmall: TextStyle = T,
                 val headlineLarge: TextStyle = T, val headlineMedium: TextStyle = T, val headlineSmall: TextStyle = T,
                 val titleLarge: TextStyle = T, val titleMedium: TextStyle = T, val titleSmall: TextStyle = T,
                 val bodyLarge: TextStyle = T, val bodyMedium: TextStyle = T, val bodySmall: TextStyle = T,
                 val labelLarge: TextStyle = T, val labelMedium: TextStyle = T, val labelSmall: TextStyle = T)
fun MaterialTheme(colorScheme: ColorScheme, typography: Typography, content: () -> Unit) = content()
