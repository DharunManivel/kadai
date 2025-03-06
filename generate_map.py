import json
import folium
from folium.plugins import MarkerCluster

def load_restaurants():
    """Load restaurant data with validation"""
    try:
        with open('restaurants.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [r for r in data if validate_restaurant(r)]
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return []

def validate_restaurant(restaurant):
    """Validate restaurant data structure"""
    required = ['name_en', 'name_ta', 'lat', 'lng', 'map_link']
    return all(key in restaurant and restaurant[key] for key in required)

def create_base_map():
    """Initialize folium map with proper error handling"""
    try:
        return folium.Map(location=[11.1271, 78.6569], zoom_start=7, tiles='cartodbpositron')
    except Exception as e:
        print(f"Map initialization failed: {str(e)}")
        raise

def add_markers(map_obj, restaurants):
    """Add markers with clustered grouping and index for details"""
    try:
        marker_cluster = MarkerCluster().add_to(map_obj)
        for idx, restaurant in enumerate(restaurants):
            folium.Marker(
                location=[restaurant['lat'], restaurant['lng']],
                popup=create_popup(restaurant, idx),
                icon=folium.Icon(color='red', icon='utensils', prefix='fa')
            ).add_to(marker_cluster)
        return True
    except Exception as e:
        print(f"Marker error: {str(e)}")
        return False

def create_popup(restaurant, idx):
    """Create safe HTML popup content with styled View Details button"""
    html = f"""
        <div>
            <b>{escape_html(restaurant['name_en'])}</b><br>
            {escape_html(restaurant.get('special_en', ''))}<br>
            <small>{restaurant.get('rating', 'N/A')} ⭐ ({restaurant.get('reviews', '0')} reviews)</small><br>
            <button class="view-details-btn" onclick="showDetails(restaurants[{idx}])">View Details</button>
        </div>
    """
    return folium.Popup(html, max_width=250)

def escape_html(text):
    """Proper HTML escaping for user-generated content"""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def add_search_components(map_obj, restaurants):
    """Add search interface and details panel with improved field handling"""
    try:
        search_html = """
        <div id="searchContainer" style="position: fixed; top: 20px; left: 20px; z-index: 1000;
              background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);
              width: 350px;">
            <input type="text" id="searchInput"
                   placeholder="🔍 Search by name or location (English/Tamil)"
                   style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;
                          font-size: 14px;">
            <div id="suggestions" style="margin-top: 10px; max-height: 400px; overflow-y: auto; display: none;"></div>
        </div>

        <div id="detailsPanel" style="position: fixed; bottom: -400px; left: 0; right: 0; background: white;
              z-index: 999; transition: all 0.3s; box-shadow: 0 -2px 15px rgba(0,0,0,0.2);
              border-radius: 15px 15px 0 0; padding: 25px 20px 20px;">
            <div id="panelContent" style="max-width: 800px; margin: 0 auto; position: relative;">
                <button onclick="closePanel()" style="position: absolute; top: -45px; right: 10px;
                        background: #fff; border: none; border-radius: 50%; width: 40px; height: 40px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer;">✕</button>
                <div id="detailsContent"></div>
            </div>
        </div>
        """

        safe_restaurants = json.dumps(restaurants, ensure_ascii=False).replace("'", "\\'").replace("</", "<\\/")

        search_js = f"""
        <script>
        const restaurants = JSON.parse('{safe_restaurants}');

        function showDetails(restaurant) {{
            try {{
                const content = `
                    <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #333;">
                        <h2 style="margin: 0 0 10px; color: #1a73e8;">${{restaurant.name_en}}</h2>
                        <h3 style="margin: 0 0 15px; color: #666; font-weight: normal;">${{restaurant.name_ta || ''}}</h3>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div>
                                <p style="margin: 8px 0;">
                                    <b style="color: #444;">📍 Location:</b><br>
                                    ${{restaurant.location_en || 'N/A'}}<br>
                                    <small style="color: #888;">${{restaurant.location_ta || ''}}</small>
                                </p>
                                <p style="margin: 8px 0;">
                                    <b style="color: #444;">📞 Phone:</b><br>
                                    ${{restaurant.phone ? `<a href="tel:${{restaurant.phone}}" style="color: #1a73e8; text-decoration: none;">${{restaurant.phone}}</a>` : 'Not available'}}
                                </p>
                            </div>
                            <div>
                                <p style="margin: 8px 0;">
                                    <b style="color: #444;">⭐ Rating:</b><br>
                                    ${{restaurant.rating ? restaurant.rating + '/5' : 'N/A'}} (${{restaurant.reviews || 0}} reviews)
                                </p>
                                <p style="margin: 8px 0;">
                                    <b style="color: #444;">🍴 Specialty:</b><br>
                                    ${{restaurant.special_en || 'No specialty listed'}}<br>
                                    <small style="color: #888;">${{restaurant.special_ta || ''}}</small>
                                </p>
                            </div>
                        </div>

                        ${{restaurant.data ? `
                            <div style="margin-top: 20px;">
                                <b style="color: #444;">📝 Description:</b>
                                <p style="margin: 8px 0; line-height: 1.5; color: #555;">
                                    ${{restaurant.data}}
                                </p>
                            </div>
                        ` : ''}}

                        <div style="margin-top: 20px; text-align: center;">
                            <a href="${{restaurant.map_link}}" target="_blank"
                               style="display: inline-block; padding: 12px 25px; background: #1a73e8; color: white;
                                      text-decoration: none; border-radius: 25px; font-weight: bold; transition: all 0.3s;"
                               onmouseover="this.style.backgroundColor='#1557b0'"
                               onmouseout="this.style.backgroundColor='#1a73e8'">
                                🗺️ Get Directions
                            </a>
                        </div>
                    </div>
                `;
                document.getElementById('detailsContent').innerHTML = content;
                document.getElementById('detailsPanel').style.bottom = '0';
                map.setView([restaurant.lat, restaurant.lng], 16);
            }} catch(e) {{
                console.error('Details error:', e);
            }}
        }}

        function closePanel() {{
            document.getElementById('detailsPanel').style.bottom = '-400px';
        }}

        function searchRestaurants(query) {{
            try {{
                const q = query.toLowerCase().trim();
                return restaurants.filter(r =>
                    (r.name_en && r.name_en.toLowerCase().includes(q)) ||
                    (r.name_ta && r.name_ta.toLowerCase().includes(q)) ||
                    (r.location_en && r.location_en.toLowerCase().includes(q)) ||
                    (r.location_ta && r.location_ta.toLowerCase().includes(q))
                );
            }} catch(e) {{
                console.error('Search error:', e);
                return [];
            }}
        }}

        function updateSuggestions() {{
            try {{
                const input = document.getElementById('searchInput').value;
                const suggestions = searchRestaurants(input);
                const suggestionsDiv = document.getElementById('suggestions');

                suggestionsDiv.innerHTML = suggestions.slice(0, 8).map((r, idx) => `
                    <div style="padding: 12px; border-bottom: 1px solid #eee; cursor: pointer;
                                transition: background 0.2s;"
                         onmouseover="this.style.background='#f8f9fa'"
                         onmouseout="this.style.background='white'"
                         onclick="showDetails(restaurants[${{restaurants.indexOf(r)}}])">
                        <div style="font-weight: 500; color: #1a73e8;">${{r.name_en}}</div>
                        <div style="font-size: 0.9em; color: #666;">${{r.location_en || 'Location not specified'}}</div>
                        <div style="font-size: 0.8em; color: #888; margin-top: 4px;">
                            ${{r.special_en || 'No specialty'}}
                        </div>
                    </div>
                `).join('');

                suggestionsDiv.style.display = input ? 'block' : 'none';
            }} catch(e) {{
                console.error('Suggestion error:', e);
            }}
        }}

        document.getElementById('searchInput').addEventListener('input', updateSuggestions);
        </script>
        """

        css = """
        <style>
            #searchInput::placeholder { color: #999; }
            #suggestions { border: 1px solid #eee; border-radius: 4px; }
            #detailsPanel { font-size: 16px; }
            #detailsPanel h2 { font-size: 24px; }
            #detailsPanel h3 { font-size: 18px; }
            #detailsContent b { display: inline-block; min-width: 80px; }
            .view-details-btn {
                margin-top: 10px;
                padding: 8px 15px;
                background: #1a73e8;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
            }
            .view-details-btn:hover {
                background: #1557b0;
            }
        </style>
        """

        map_obj.get_root().html.add_child(folium.Element(search_html))
        map_obj.get_root().html.add_child(folium.Element(search_js))
        map_obj.get_root().html.add_child(folium.Element(css))
        return True
    except Exception as e:
        print(f"Search component error: {str(e)}")
        return False

def main():
    """Main execution flow"""
    restaurants = load_restaurants()
    if not restaurants:
        print("No valid restaurant data to display")
        return

    m = create_base_map()
    if not add_markers(m, restaurants):
        print("Failed to add markers")
        return

    if not add_search_components(m, restaurants):
        print("Failed to add search components")
        return

    try:
        m.save('tamilnadu_food_map.html')
        print("Map generated successfully: tamilnadu_food_map.html")
    except Exception as e:
        print(f"Save failed: {str(e)}")

if __name__ == "__main__":
    main()
