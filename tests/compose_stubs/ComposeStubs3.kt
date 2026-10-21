@file:Suppress("unused", "UNUSED_PARAMETER")
package androidx.compose.ui.graphics
class Color(val value: ULong)
fun Color(color: Long): Color = Color(color.toULong())
