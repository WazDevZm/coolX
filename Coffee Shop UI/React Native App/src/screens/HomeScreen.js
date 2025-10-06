import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Dimensions,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';
import * as Animatable from 'react-native-animatable';

const { width } = Dimensions.get('window');

const HomeScreen = ({ navigation }) => {
  const featuredProducts = [
    {
      id: 1,
      name: 'Cappuccino',
      price: '$4.50',
      image: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Perfect balance of espresso, steamed milk, and foam',
    },
    {
      id: 2,
      name: 'Latte',
      price: '$5.00',
      image: 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Smooth and creamy with a hint of sweetness',
    },
    {
      id: 3,
      name: 'Espresso',
      price: '$3.50',
      image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Rich, bold, and perfectly extracted',
    },
  ];

  const quickActions = [
    { title: 'Order Now', icon: 'coffee', color: '#8B4513', screen: 'Menu' },
    { title: 'Find Store', icon: 'location-on', color: '#654321', screen: 'StoreLocator' },
    { title: 'My Orders', icon: 'history', color: '#8B4513', screen: 'OrderHistory' },
    { title: 'Rewards', icon: 'card-giftcard', color: '#654321', screen: 'Profile' },
  ];

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <LinearGradient
        colors={['#8B4513', '#654321']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.greeting}>Good Morning!</Text>
            <Text style={styles.userName}>Welcome to Brew & Bean</Text>
          </View>
          <TouchableOpacity style={styles.notificationBtn}>
            <Icon name="notifications" size={24} color="#fff" />
          </TouchableOpacity>
        </View>
      </LinearGradient>

      {/* Quick Actions */}
      <Animatable.View animation="fadeInUp" delay={300} style={styles.quickActions}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <View style={styles.actionsGrid}>
          {quickActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.actionCard, { backgroundColor: action.color }]}
              onPress={() => navigation.navigate(action.screen)}
            >
              <Icon name={action.icon} size={30} color="#fff" />
              <Text style={styles.actionText}>{action.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </Animatable.View>

      {/* Featured Products */}
      <Animatable.View animation="fadeInUp" delay={500} style={styles.featuredSection}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Featured Today</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Menu')}>
            <Text style={styles.seeAllText}>See All</Text>
          </TouchableOpacity>
        </View>
        
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.productsScroll}>
          {featuredProducts.map((product, index) => (
            <TouchableOpacity
              key={product.id}
              style={styles.productCard}
              onPress={() => navigation.navigate('ProductDetail', { product })}
            >
              <Image source={{ uri: product.image }} style={styles.productImage} />
              <View style={styles.productInfo}>
                <Text style={styles.productName}>{product.name}</Text>
                <Text style={styles.productDescription}>{product.description}</Text>
                <Text style={styles.productPrice}>{product.price}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </Animatable.View>

      {/* Promotions */}
      <Animatable.View animation="fadeInUp" delay={700} style={styles.promotionSection}>
        <LinearGradient
          colors={['#8B4513', '#654321']}
          style={styles.promotionCard}
        >
          <View style={styles.promotionContent}>
            <Text style={styles.promotionTitle}>Special Offer!</Text>
            <Text style={styles.promotionText}>
              Get 20% off on your first order. Use code: WELCOME20
            </Text>
            <TouchableOpacity style={styles.promotionBtn}>
              <Text style={styles.promotionBtnText}>Claim Now</Text>
            </TouchableOpacity>
          </View>
          <Icon name="local-offer" size={60} color="#fff" style={styles.promotionIcon} />
        </LinearGradient>
      </Animatable.View>

      {/* Store Info */}
      <Animatable.View animation="fadeInUp" delay={900} style={styles.storeInfo}>
        <Text style={styles.sectionTitle}>Visit Our Store</Text>
        <View style={styles.storeCard}>
          <View style={styles.storeDetails}>
            <Text style={styles.storeName}>Brew & Bean Coffee</Text>
            <Text style={styles.storeAddress}>123 Coffee Street, Downtown</Text>
            <Text style={styles.storeHours}>Open: 6:00 AM - 8:00 PM</Text>
          </View>
          <TouchableOpacity 
            style={styles.directionsBtn}
            onPress={() => navigation.navigate('StoreLocator')}
          >
            <Icon name="directions" size={20} color="#8B4513" />
            <Text style={styles.directionsText}>Directions</Text>
          </TouchableOpacity>
        </View>
      </Animatable.View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    paddingTop: 50,
    paddingBottom: 30,
    paddingHorizontal: 20,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  greeting: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 5,
  },
  notificationBtn: {
    padding: 10,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  quickActions: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionCard: {
    width: (width - 60) / 2,
    height: 100,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  actionText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    marginTop: 8,
  },
  featuredSection: {
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  seeAllText: {
    color: '#8B4513',
    fontSize: 16,
    fontWeight: '600',
  },
  productsScroll: {
    marginHorizontal: -20,
  },
  productCard: {
    width: 200,
    backgroundColor: '#fff',
    borderRadius: 15,
    marginRight: 15,
    marginLeft: 20,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    overflow: 'hidden',
  },
  productImage: {
    width: '100%',
    height: 120,
    resizeMode: 'cover',
  },
  productInfo: {
    padding: 15,
  },
  productName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  productDescription: {
    fontSize: 12,
    color: '#666',
    marginBottom: 8,
    lineHeight: 16,
  },
  productPrice: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#8B4513',
  },
  promotionSection: {
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  promotionCard: {
    borderRadius: 15,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  promotionContent: {
    flex: 1,
  },
  promotionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  promotionText: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
    marginBottom: 15,
    lineHeight: 20,
  },
  promotionBtn: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 20,
    alignSelf: 'flex-start',
  },
  promotionBtnText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  promotionIcon: {
    opacity: 0.3,
  },
  storeInfo: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  storeCard: {
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  storeDetails: {
    flex: 1,
  },
  storeName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  storeAddress: {
    fontSize: 14,
    color: '#666',
    marginBottom: 3,
  },
  storeHours: {
    fontSize: 14,
    color: '#8B4513',
    fontWeight: '600',
  },
  directionsBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
  },
  directionsText: {
    color: '#8B4513',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 5,
  },
});

export default HomeScreen;



