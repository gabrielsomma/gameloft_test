from flask import Blueprint, request, jsonify
from models import Profile, profiles, Campaign, campaigns

routes = Blueprint('routes', __name__)


@routes.route('/profiles', methods=['POST'])
def add_profile():
    player_id = request.json['player_id']
    active_campaign = request.json['active_campaign']
    level = request.json['level']
    country = request.json['country']
    inventory = request.json['inventory']
    new_profile = Profile(player_id, active_campaign, int(level), country, inventory)

    matched_index = next((i for i, profile in enumerate(profiles) if profile.player_id == new_profile.player_id), None)
    if matched_index is None:
        profiles.append(new_profile)
    else:
        profiles[matched_index] = new_profile

    return jsonify(new_profile.__dict__)


@routes.route('/campaigns', methods=['POST'])
def add_campaign():
    name = request.json['name']
    matchers = request.json['matchers']
    new_campaign = Campaign(name, matchers)

    matched_index = next((i for i, campaign in enumerate(campaigns) if campaign.name == new_campaign.name), None)
    if matched_index is None:
        campaigns.append(new_campaign)
    else:
        campaigns[matched_index] = new_campaign

    return jsonify(new_campaign.__dict__)


@routes.route('/profiles', methods=['GET'])
def get_profiles():
    return jsonify(profiles=[p.__dict__ for p in profiles])


@routes.route('/campaigns', methods=['GET'])
def get_campaigns():
    return jsonify(campaigns=[c.__dict__ for c in campaigns])


@routes.route('/profile/<id>', methods=['GET'])
def get_profile(id):
    for profile in profiles:
        if profile.player_id == str(id):
            campaign_index = next(iter(campaigns), None)
            if campaign_index is None:
                return jsonify({"message": "No active campaigns"}), 404
            if campaigns[campaign_index].match_profile(profile):
                return jsonify(profile.__dict__)
    return jsonify({"message": "Product not found"}), 404
