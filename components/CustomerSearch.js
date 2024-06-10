import React, { useState } from 'react';
import { View, Text, Button, TextInput } from 'react-native';
import { searchCustomer } from '../backend/services/apiService';

const CustomerSearch = () => {
    const [search, setSearch] = useState('');
    const [customerDetails, setCustomerDetails] = useState(null);

    const handleSearch = async () => {
        try {
            const data = await searchCustomer(search);
            setCustomerDetails(data);
        } catch (error) {
            console.error('Error fetching customer details:', error);
        }
    };

    return (
        <View>
            <TextInput
                placeholder="Search Customer"
                value={search}
                onChangeText={setSearch}
            />
            <Button title="Search" onPress={handleSearch} />
            {customerDetails && (
                <Text>{JSON.stringify(customerDetails, null, 2)}</Text>
            )}
        </View>
    );
};

export default CustomerSearch;
