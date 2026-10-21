import React from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Heart } from 'lucide-react-native';
import Animated, { FadeInDown, withSpring } from 'react-native-reanimated';

export default function Home() {
  return (
    <View style={styles.root}>
      <Text allowFontScaling={false} style={styles.title}>Hi Sam 👋</Text>
      <Pressable onPress={() => {}}>
        <Ionicons name="menu" size={22} />
      </Pressable>
      <Animated.View entering={FadeInDown}><Text>Trusted by 50k+ users</Text></Animated.View>
      <View className="bg-gradient-to-r from-purple-500 to-pink-500 h-screen" />
      <Heart />
    </View>
  );
}

const styles = StyleSheet.create({
  root: { padding: 13, gap: 10, backgroundColor: '#0B0B0F' },
  title: { fontSize: 29, color: '#F5F5F5', textAlign: 'center' },
});
