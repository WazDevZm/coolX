import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  TextInput,
  FlatList,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import * as Animatable from 'react-native-animatable';

const MenuScreen = ({ navigation }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  const categories = ['All', 'Coffee', 'Pastries', 'Sandwiches', 'Beverages'];

  const menuItems = [
    {
      id: 1,
      name: 'Espresso',
      category: 'Coffee',
      price: 3.50,
      image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Rich, bold, and perfectly extracted',
      rating: 4.8,
      preparationTime: '2-3 min',
    },
    {
      id: 2,
      name: 'Cappuccino',
      category: 'Coffee',
      price: 4.50,
      image: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Perfect balance of espresso, steamed milk, and foam',
      rating: 4.9,
      preparationTime: '3-4 min',
    },
    {
      id: 3,
      name: 'Latte',
      category: 'Coffee',
      price: 5.00,
      image: 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Smooth and creamy with a hint of sweetness',
      rating: 4.7,
      preparationTime: '3-4 min',
    },
    {
      id: 4,
      name: 'Americano',
      category: 'Coffee',
      price: 3.00,
      image: 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Bold espresso with hot water for a clean taste',
      rating: 4.6,
      preparationTime: '2-3 min',
    },
    {
      id: 5,
      name: 'Butter Croissant',
      category: 'Pastries',
      price: 2.50,
      image: 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Flaky, buttery, and perfectly golden',
      rating: 4.8,
      preparationTime: '1-2 min',
    },
    {
      id: 6,
      name: 'Blueberry Muffin',
      category: 'Pastries',
      price: 3.00,
      image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Fresh baked with real blueberries',
      rating: 4.7,
      preparationTime: '1-2 min',
    },
    {
      id: 7,
      name: 'Turkey & Avocado Sandwich',
      category: 'Sandwiches',
      price: 8.50,
      image: 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Fresh turkey with avocado and sprouts',
      rating: 4.9,
      preparationTime: '5-7 min',
    },
    {
      id: 8,
      name: 'Green Smoothie',
      category: 'Beverages',
      price: 6.50,
      image: 'https://images.unsplash.com/photo-1571934811356-5cc061b6821f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
      description: 'Fresh spinach, banana, and mango',
      rating: 4.5,
      preparationTime: '3-4 min',
    },
  ];

  const filteredItems = menuItems.filter(item => {
    const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const renderMenuItem = ({ item, index }) => (
    <Animatable.View
      animation="fadeInUp"
      delay={index * 100}
      style={styles.menuItem}
    >
      <TouchableOpacity
        style={styles.menuItemContent}
        onPress={() => navigation.navigate('ProductDetail', { product: item })}
      >
        <Image source={{ uri: item.image }} style={styles.menuItemImage} />
        <View style={styles.menuItemInfo}>
          <View style={styles.menuItemHeader}>
            <Text style={styles.menuItemName}>{item.name}</Text>
            <View style={styles.ratingContainer}>
              <Icon name="star" size={14} color="#FFD700" />
              <Text style={styles.rating}>{item.rating}</Text>
            </View>
          </View>
          <Text style={styles.menuItemDescription}>{item.description}</Text>
          <View style={styles.menuItemFooter}>
            <Text style={styles.menuItemPrice}>${item.price.toFixed(2)}</Text>
            <View style={styles.prepTimeContainer}>
              <Icon name="access-time" size={14} color="#666" />
              <Text style={styles.prepTime}>{item.preparationTime}</Text>
            </View>
          </View>
        </View>
        <TouchableOpacity style={styles.addButton}>
          <Icon name="add" size={20} color="#8B4513" />
        </TouchableOpacity>
      </TouchableOpacity>
    </Animatable.View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Our Menu</Text>
        <TouchableOpacity style={styles.filterBtn}>
          <Icon name="tune" size={24} color="#8B4513" />
        </TouchableOpacity>
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <View style={styles.searchBar}>
          <Icon name="search" size={20} color="#666" />
          <TextInput
            style={styles.searchInput}
            placeholder="Search menu items..."
            value={searchQuery}
            onChangeText={setSearchQuery}
            placeholderTextColor="#999"
          />
          {searchQuery.length > 0 && (
            <TouchableOpacity onPress={() => setSearchQuery('')}>
              <Icon name="clear" size={20} color="#666" />
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Category Filter */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.categoryContainer}
        contentContainerStyle={styles.categoryContent}
      >
        {categories.map((category, index) => (
          <TouchableOpacity
            key={index}
            style={[
              styles.categoryBtn,
              selectedCategory === category && styles.categoryBtnActive
            ]}
            onPress={() => setSelectedCategory(category)}
          >
            <Text
              style={[
                styles.categoryText,
                selectedCategory === category && styles.categoryTextActive
              ]}
            >
              {category}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Menu Items */}
      <FlatList
        data={filteredItems}
        renderItem={renderMenuItem}
        keyExtractor={item => item.id.toString()}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.menuList}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Icon name="search-off" size={60} color="#ccc" />
            <Text style={styles.emptyText}>No items found</Text>
            <Text style={styles.emptySubtext}>Try adjusting your search or filters</Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 10,
    backgroundColor: '#fff',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  filterBtn: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
  },
  searchContainer: {
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#fff',
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    borderRadius: 25,
    paddingHorizontal: 15,
    paddingVertical: 12,
  },
  searchInput: {
    flex: 1,
    marginLeft: 10,
    fontSize: 16,
    color: '#333',
  },
  categoryContainer: {
    backgroundColor: '#fff',
    paddingVertical: 15,
  },
  categoryContent: {
    paddingHorizontal: 20,
  },
  categoryBtn: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
    marginRight: 10,
  },
  categoryBtnActive: {
    backgroundColor: '#8B4513',
  },
  categoryText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
  },
  categoryTextActive: {
    color: '#fff',
  },
  menuList: {
    padding: 20,
  },
  menuItem: {
    marginBottom: 15,
    backgroundColor: '#fff',
    borderRadius: 15,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  menuItemContent: {
    flexDirection: 'row',
    padding: 15,
    alignItems: 'center',
  },
  menuItemImage: {
    width: 80,
    height: 80,
    borderRadius: 10,
    marginRight: 15,
  },
  menuItemInfo: {
    flex: 1,
  },
  menuItemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 5,
  },
  menuItemName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rating: {
    fontSize: 12,
    color: '#666',
    marginLeft: 3,
  },
  menuItemDescription: {
    fontSize: 12,
    color: '#666',
    marginBottom: 8,
    lineHeight: 16,
  },
  menuItemFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  menuItemPrice: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#8B4513',
  },
  prepTimeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  prepTime: {
    fontSize: 12,
    color: '#666',
    marginLeft: 3,
  },
  addButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 10,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 50,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
    marginTop: 15,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    marginTop: 5,
  },
});

export default MenuScreen;

