SOURCE_FILE = 'numbers.txt'


def get_region_volume(region):
  return (region[1] - region[0] + 1) * (region[3] - region[2] + 1) * (region[5] - region[4] + 1)


def is_intersecting(region1, region2):
  return region1[0] <= region2[1] and region2[0] <= region1[1] and \
         region1[2] <= region2[3] and region2[2] <= region1[3] and \
         region1[4] <= region2[5] and region2[4] <= region1[5]


def get_intersecting_region(region1, region2):
  return [
    max(region1[0], region2[0]),
    min(region1[1], region2[1]),
    max(region1[2], region2[2]),
    min(region1[3], region2[3]),
    max(region1[4], region2[4]),
    min(region1[5], region2[5]),
  ]


def get_overlapping_regions(existing_regions, positive_region, region):
  new_regions = []
  for existing_positive_region, existing_region in existing_regions:
    # New positive overlaps negative -> add if previous negative
    if (not existing_positive_region) and positive_region:
      if is_intersecting(existing_region, region):
        new_regions.append((True, get_intersecting_region(existing_region, region)))

    # 2 negatives -> add positive for overlapping region
    if (not existing_positive_region) and (not positive_region):
      if is_intersecting(existing_region, region):
        new_regions.append((True, get_intersecting_region(existing_region, region)))

    # New negative overlaps positive -> add negative for region overlapping
    if existing_positive_region and (not positive_region):
      if is_intersecting(existing_region, region):
        new_regions.append((False, get_intersecting_region(existing_region, region)))

    # 2 positives overlap, need to add a negative for region overlapping
    if existing_positive_region and positive_region:
      if is_intersecting(existing_region, region):
        new_regions.append((False, get_intersecting_region(existing_region, region)))

  if positive_region:
    new_regions.append((positive_region, region))
  return new_regions


def run():
  regions = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      on_off, coords = line.strip().split(' ')
      regions.append(
        (on_off == 'on', [int(value) for bounds in coords.strip().split(',') for value in bounds[2:].split('..')]))

  all_regions = []
  for positive_region, region in regions:
    if all([abs(value) <= 50 for value in region]):
      all_regions += get_overlapping_regions(all_regions, positive_region, region)

  region_volumes = [get_region_volume(region) * (1 if positive_region else -1) for positive_region, region in
                    all_regions]
  print(sum(region_volumes))


if __name__ == '__main__':
  run()
